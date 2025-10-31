import os
import pwd
import grp
import subprocess
import random

def test_group_exists():
    """Check if the 'devteam' group exists."""
    grp.getgrnam("devteam")  # will raise KeyError if missing

def test_users_exist_and_in_group():
    """Check if users exist and belong to 'devteam'."""
    for user in ["aubrey", "margarette"]:
        pwd.getpwnam(user)  # raises KeyError if missing
        groups = [g.gr_name for g in grp.getgrall() if user in g.gr_mem]
        assert "devteam" in groups, f"{user} not in devteam group"

def test_shared_directory_permissions():
    """Check /shared/dev permissions."""
    path = "/shared/dev"
    assert os.path.isdir(path), f"{path} does not exist"

    stat_info = os.stat(path)
    group = grp.getgrgid(stat_info.st_gid).gr_name
    assert group == "devteam", f"{path} group owner should be 'devteam', found '{group}'"
    
    mode = oct(stat_info.st_mode)[-4:]
    assert mode == "2770", f"{path} permissions should be 2770, found {mode}"

def test_users_can_create_files():
    """Users create multiple files to ensure proper setup."""
    path = "/shared/dev"
    for user in ["aubrey", "margarette"]:
        for i in range(3):
            test_file = os.path.join(path, f"{user}_check_{i}.txt")
            subprocess.run(["su", "-", user, "-c", f"touch {test_file}"], check=True)
            # check permissions immediately
            stat_info = os.stat(test_file)
            group = grp.getgrgid(stat_info.st_gid).gr_name
            assert group == "devteam", f"{test_file} group should be 'devteam'"
            assert stat_info.st_mode & 0o060, f"{test_file} should have group read/write"
            os.remove(test_file)

def test_users_can_edit_files():
    """Check editing and setgid inheritance."""
    path = "/shared/dev"
    users = ["aubrey", "margarette"]

    for user in users:
        test_file = os.path.join(path, f"{user}_edit_check.txt")
        subprocess.run(["su", "-", user, "-c", f"touch {test_file}"], check=True)
        for _ in range(random.randint(1,3)):
            subprocess.run(["su", "-", user, "-c", f"echo 'edit' >> {test_file}"], check=True)

        # Ensure group ownership is correct
        stat_info = os.stat(test_file)
        group = grp.getgrgid(stat_info.st_gid).gr_name
        assert group == "devteam", f"{test_file} group should be 'devteam'"

        # Cross-user check: other devteam member can read/write
        for other in users:
            if other == user:
                continue
            # read
            result = subprocess.run(["su", "-", other, "-c", f"cat {test_file}"], capture_output=True, text=True)
            assert "edit" in result.stdout, f"{other} cannot read {test_file} created by {user}"
            # write
            subprocess.run(["su", "-", other, "-c", f"echo 'append' >> {test_file}"], check=True)

        os.remove(test_file)
