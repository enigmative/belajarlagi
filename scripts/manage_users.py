"""Manage Belajar Lagi accounts.

Accounts are created by an admin (no public registration yet).

Examples:
    python scripts/manage_users.py setup-admin --email admin@example.com --name Admin
    python scripts/manage_users.py ensure-admin
    python scripts/manage_users.py create --email siswa@example.com --name Siswa
    python scripts/manage_users.py reset-password --email siswa@example.com
    python scripts/manage_users.py list
"""
import argparse
import getpass
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.services import auth, db  # noqa: E402
from database.database import init_db  # noqa: E402


def _read_password() -> str:
    password = getpass.getpass("Password: ")
    confirm = getpass.getpass("Ulangi password: ")
    if password != confirm:
        raise SystemExit("Password tidak sama.")
    if len(password) < 8:
        raise SystemExit("Password minimal 8 karakter.")
    return password


def _password_from_args(args) -> str:
    if args.password:
        if len(args.password) < 8:
            raise SystemExit("Password minimal 8 karakter.")
        return args.password
    if not sys.stdin.isatty():
        raise SystemExit("Gunakan --password saat berjalan non-interaktif.")
    return _read_password()


def _user_by_email(email: str) -> dict:
    user = db.get_user_by_email(email)
    if not user:
        raise SystemExit(f"User {email} tidak ditemukan.")
    return user


def cmd_setup_admin(args):
    email = args.email.strip().lower()
    name = args.name.strip()
    existing = db.get_user_by_email(email)
    legacy = db.get_legacy_owner()

    if existing and (not legacy or existing["id"] != legacy["id"]):
        raise SystemExit(f"Email {email} sudah dipakai akun lain.")

    password_hash = auth.hash_password(_password_from_args(args))
    if legacy:
        db.update_user(legacy["id"], email, name, "admin", password_hash)
        print(f"Admin siap: {email} (akun legacy {legacy['id']} diklaim).")
    else:
        user_id = db.create_user(email, name, password_hash, role="admin")
        print(f"Admin dibuat: {email} (id {user_id}).")


def _prompt_admin_details(legacy: dict | None) -> tuple[str, str, str]:
    if not sys.stdin.isatty():
        raise SystemExit(
            "Belum ada admin. Jalankan setup-admin dengan --email, --name, dan --password."
        )
    if legacy:
        print("Database lama terdeteksi. Akun owner@local akan diklaim.")
    print("Buat akun admin pertama.")
    try:
        email = input("Email admin: ").strip().lower()
        if "@" not in email:
            raise SystemExit("Email tidak valid.")
        name = input("Nama admin: ").strip()
        if not name:
            raise SystemExit("Nama tidak boleh kosong.")
        password = _read_password()
    except EOFError:
        raise SystemExit(
            "Input admin tidak tersedia. Jalankan setup-admin dengan --email, --name, dan --password."
        ) from None
    return email, name, password


def cmd_ensure_admin(_args):
    for listed in db.list_users():
        user = db.get_user_by_id(listed["id"])
        if (
            user
            and user["role"] == "admin"
            and user["is_active"]
            and user["password_hash"] not in (None, "", "!")
        ):
            print(f"Admin sudah siap: {user['email']}")
            return

    legacy = db.get_legacy_owner()
    email, name, password = _prompt_admin_details(legacy)
    if legacy:
        db.update_user(legacy["id"], email, name, "admin", auth.hash_password(password))
        print(f"Admin siap: {email} (akun legacy {legacy['id']} diklaim).")
    else:
        user_id = db.create_user(email, name, auth.hash_password(password), role="admin")
        print(f"Admin dibuat: {email} (id {user_id}).")


def cmd_create(args):
    email = args.email.strip().lower()
    if db.get_user_by_email(email):
        raise SystemExit(f"Email {email} sudah terdaftar.")
    password_hash = auth.hash_password(_password_from_args(args))
    role = "admin" if args.admin else "user"
    user_id = db.create_user(email, args.name.strip(), password_hash, role=role)
    print(f"Akun {role} dibuat: {email} (id {user_id}).")


def cmd_reset_password(args):
    user = _user_by_email(args.email.strip().lower())
    password_hash = auth.hash_password(_password_from_args(args))
    db.set_user_password(user["id"], password_hash)
    db.delete_user_sessions(user["id"])
    print(f"Password {user['email']} diperbarui. Semua sesi lama logout.")


def cmd_set_active(args, active: bool):
    user = _user_by_email(args.email.strip().lower())
    db.set_user_active(user["id"], active)
    if not active:
        db.delete_user_sessions(user["id"])
    print(f"Akun {user['email']} {'diaktifkan' if active else 'dinonaktifkan'}.")


def cmd_list(_args):
    users = db.list_users()
    if not users:
        print("Belum ada akun.")
        return
    print(f"{'ID':>4}  {'ROLE':<5}  {'AKTIF':<5}  {'EMAIL':<32}  NAMA")
    for user in users:
        print(
            f"{user['id']:>4}  {user['role']:<5}  "
            f"{'ya' if user['is_active'] else 'tidak':<5}  "
            f"{user['email']:<32}  {user['name']}"
        )


def build_parser():
    parser = argparse.ArgumentParser(description="Kelola akun Belajar Lagi.")
    sub = parser.add_subparsers(dest="command", required=True)

    admin = sub.add_parser("setup-admin", help="Buat/klaim akun admin pertama.")
    admin.add_argument("--email", required=True)
    admin.add_argument("--name", required=True)
    admin.add_argument("--password")
    admin.set_defaults(func=cmd_setup_admin)

    ensure = sub.add_parser("ensure-admin", help="Prompt pembuatan admin jika belum ada.")
    ensure.set_defaults(func=cmd_ensure_admin)

    create = sub.add_parser("create", help="Buat akun baru.")
    create.add_argument("--email", required=True)
    create.add_argument("--name", required=True)
    create.add_argument("--admin", action="store_true")
    create.add_argument("--password")
    create.set_defaults(func=cmd_create)

    reset = sub.add_parser("reset-password", help="Reset password akun.")
    reset.add_argument("--email", required=True)
    reset.add_argument("--password")
    reset.set_defaults(func=cmd_reset_password)

    activate = sub.add_parser("activate", help="Aktifkan akun.")
    activate.add_argument("--email", required=True)
    activate.set_defaults(func=lambda a: cmd_set_active(a, True))

    deactivate = sub.add_parser("deactivate", help="Nonaktifkan akun.")
    deactivate.add_argument("--email", required=True)
    deactivate.set_defaults(func=lambda a: cmd_set_active(a, False))

    listing = sub.add_parser("list", help="Tampilkan semua akun.")
    listing.set_defaults(func=cmd_list)
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    init_db()
    args.func(args)


if __name__ == "__main__":
    main()
