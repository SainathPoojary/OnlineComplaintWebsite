function logout(){
    print("worked")
    document.cookie = "username=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    location.reload()
    print("worked")
}

