# from urllib import response
from fastapi import Depends, FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from itsdangerous import  URLSafeTimedSerializer
from motor.motor_asyncio import AsyncIOMotorClient
import datetime
import random
import uvicorn
from starlette.responses import RedirectResponse
from dependencies import get_current_user
from admin_router import router as adminrouter
from user_router import router as userrouter
from dependencies_adm import get_current_admin

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app= FastAPI()


# origins = [
#     "https://happy-tree-0b5e39e10.5.azurestaticapps.net",
#     "http://localhost:8000",  # Add your local development URL
#     "http://127.0.0.1:8000"  # Add alternative local URL
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=False, 
)





app.include_router(adminrouter, prefix="/admin")
app.include_router(userrouter, prefix="/users")

SECRET_KEY = "sdsfe45456@21!!"
serializer = URLSafeTimedSerializer(SECRET_KEY)



# connecting to db
client= AsyncIOMotorClient("mongodb+srv://jwdidrees:6523xsHvypiSDdXe@cluster0.79mxm.mongodb.net/")
db= client.Bank 
users_collection = db.users 
template= Jinja2Templates(directory="templates")



@app.get("/")
async def home(request : Request):
    return template.TemplateResponse("Signin.html" ,{ "request" : request})


#=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-Sign In=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

    


@app.post("/user/sign_in")
async def login(request: Request):
    x = 0
    form_data = await request.form()
    login_email = str(form_data.get("log_email"))
    login_pass =  str(form_data.get("log_pass"))
    
#    =================== For Admin===========================
    admin_email = "afnanajmal@gmail.com"
    admin_password = "Afnan@123"
    if login_email == admin_email and login_pass == admin_password:
        response = RedirectResponse(url="/admin/admin_main/admin", status_code= 303)
        session_data = {"Email": admin_email}
        session_cookie = serializer.dumps(session_data)
        response.set_cookie("admin", session_cookie)
        return response
    
  #======================For Normal Users====================== 
    user = await db.users.find_one({"Email": login_email})

    if user and user["Password"] == login_pass:
        
        response = RedirectResponse(url="/users/users_main/user", status_code= 303)
        session_data = {"Email": login_email}
        session_cookie = serializer.dumps(session_data)
        response.set_cookie("session", session_cookie)
        return response
    else:
        x = 1
        return template.TemplateResponse("Signin.html", {"request" : request, "x" : x})
    
#=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def generate_account_number():
        return random.randint(10000, 99999)



@app.post("/user/sign_up")
async def sign_up(request : Request):
    x = 0
    response= await request.json()
    su_name = str(response.get("username"))
    su_email = str(response.get("email"))
    su_pass = str(response.get("password"))
    su_cpass = str(response.get("confirmPassword"))
    if su_pass != su_cpass:
        return {"error": "Passwords do not match"}  

    if await db.users.find_one({"Email": su_email}):
        return {"error": "Email address already exists"} 
    

    
    su_account = generate_account_number()  
    sent =[]
    recieve =[]
    
    await db.users.insert_one({
        "Username" : su_name,
        "Email" : su_email,
        "Password" : su_pass,
        "Account" : su_account,
        "balance": 0,
        "Sent" : sent,
        "Recieve" : recieve

        
    })
    



#=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


@app.get("/signup")
async def Register_here(request: Request, response_class=HTMLResponse):
    
    return template.TemplateResponse("Signup.html", {"request": request})



#=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


@app.get("/signin")
async def Signin_here(request: Request):
    return template.TemplateResponse("Signin.html", {"request": request})

#=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


app.mount("/static", StaticFiles(directory="templates/Styles"), name="static")




@app.get("/logout", response_class=HTMLResponse)
async def logout(request : Request):
    response = RedirectResponse(url= "/signin")
    new = request.cookies.get("session")
    old = request.cookies.get("admin")
    print(old)
    print(new)
    response.delete_cookie("session")
    response.delete_cookie("admin")
    new = request.cookies.get("session")
    old = request.cookies.get("admin")
    print(old)
    print(new)
    return response



    

