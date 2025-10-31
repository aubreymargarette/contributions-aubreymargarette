import os
import pwd
import grp
import subprocess

def test_group_exists():
    """Check if the 'devteam' group exists."""
    try:
        grp.getgrnam("devteam")
    except KeyError:
        raise AssertionError("Group 'devteam' does not exist.")

def test_users_exist_and_in_group():
    """Check if users 'aubrey' and 'margarette' exist and belong to 'devteam'."""
    for user in ["aubrey", "margarette"]:
        try:
            user_info = pwd.getpwnam(user)
        except KeyError:
            raise AssertionError(f"User '{user}' does not exist.")
        
        groups = [g.gr_name for g in grp.getgrall() if user in g.gr_mem]
        if "devteam" not in groups:
            raise AssertionError(f"User '{user}' is not in the 'devteam' group.")

def test_shared_directory_permissions():
    """Check if /shared/dev exists and has correct group and permissions."""
    path = "/shared/dev"
    assert os.path.isdir(path), f"{path} directory does not exist."

    stat_info = os.stat(path)
    group = grp.getgrgid(stat_info.st_gid).gr_name
    assert group == "devteam", f"{path} group owner should be 'devteam' but is '{group}'."

    # Check permissions (2770)
    mode = oct(stat_info.st_mode)[-4:]
    assert mode == "2770", f"{path} permissions should be 2770 but are {mode}."

def test_users_can_create_files():
    """Verify that both users can create files in /shared/dev."""
    path = "/shared/dev"
    for user in ["aubrey", "margarette"]:
        test_file = os.path.join(path, f"{user}_check.txt")
        try:
            subprocess.run(["su", "-", user, "-c", f"touch {test_file}"], check=True)
            assert os.path.exists(test_file), f"{user} could not create file."
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)