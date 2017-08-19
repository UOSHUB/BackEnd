from .get import page


# Gets student's directory profile page
def dir_profile(session):
    # Coming from "Personal Information" page
    return page("bwgkoprf.P_ShowDiroItems", "GenMnu", session)
