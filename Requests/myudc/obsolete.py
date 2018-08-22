from .get import page


# Gets student's directory profile page
def dir_profile(session):
    # Coming from "Personal Information" page
    return page("bwgkoprf.P_ShowDiroItems", "GenMnu", session)


# Gets student's account summary page
# ether all terms combined or one by one (by_term=True)
def account_summary(session, by_term=False):
    # Coming from "Student Account" page
    return page("bwskoacc.P_ViewAcct" + ["Total", ''][by_term], "ARMnu", session)
