from .route import testing



@testing.get("/test")
def gett():
    return "hello this is testing"
