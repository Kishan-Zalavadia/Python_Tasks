from fastapi import FastAPI,Depends,status,HTTPException
from models import resource,project,resourceAssignment
import models
from shemas import inptut_resource,input_project
from sqlalchemy import or_
from sqlalchemy.orm import Session
from database import get_db,engine
from datetime import datetime
import uuid

app = FastAPI()

# to create database
@app.on_event("startup")
def on_startup():
    print("application started")
    models.Base.metadata.create_all(bind=engine)

# get all resources
@app.get("/resource/")
def get_resource(db:Session=Depends(get_db)):
    res = db.query(resource).filter(resource.isActive == True).all()
    if not res:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"NO data Available in resource")
    return res

# get resource by id
@app.get("/resource/{id}")
def get_resource_byid(id:uuid.UUID,db:Session=Depends(get_db)):
    res = db.query(resource).filter(resource.id == id and resource.isActive == True).first()
    return res

# create resource
@app.post("/resource/")
def create_resource(item:inptut_resource,db:Session=Depends(get_db)):
    db_resource= resource(**item.model_dump())
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return {"message":"Resource created successfully","resource":{db_resource}}

# delete resource
@app.delete("/resource/{id}")
def delete_resource(id:uuid.UUID,db:Session=Depends(get_db)):
    db_resource = db.query(resource).filter(resource.id == id and resource.isActive == True).first()
    db_resource.isActive = False
    db.commit()
    return{"message":"resource deleted Successfully"}

# get all resources in project
@app.get("/project/resource/{id}")
def resources_projects(id:uuid.UUID,db:Session=Depends(get_db)):
    db_projects = db.query(resource).join(resourceAssignment).where(resourceAssignment.projectId == id,resource.id == resourceAssignment.resourceId).all()
    return db_projects

# check resource on bench or not
@app.get("/resource/onbench/{id}")
def get_resource_satus(id:uuid.UUID,db:Session=Depends(get_db)):
    result  = db.query(resource).join(resourceAssignment,resource.id == resourceAssignment.resourceId and resourceAssignment.offBoarding == None).filter(resource.id == id).first()
    if result is None:
        return {"message":"resources is on bench "}
    return {"message":"resource is on work","data":result}

# get all onbench resources
@app.get("/resources/onbench")
def get_onboard_resource(db:Session=Depends(get_db)):
    result = db.query(resource).outerjoin(resourceAssignment,resource.id==resourceAssignment.resourceId).filter(or_(resourceAssignment.id == None , resourceAssignment.offBoarding != None)).all()
    if not result:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"NO resource onbench")
    return result

# get all projects
@app.get("/project/")
def get_project(db:Session=Depends(get_db)):
    db_project = db.query(project).all()
    if not db_project:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"NO data Available in projct")
    return db_project

# get project by id
@app.get("/project/{id}")
def get_project_byid(id:uuid.UUID,db:Session=Depends(get_db)):
    db_project = db.query(project).filter(project.id == id).one()
    return db_project

# creaete project
@app.post("/project/",status_code=status.HTTP_201_CREATED)
def create_project(item:input_project,db:Session=Depends(get_db)):
    db_project = project(name = item.name,projectManager = item.projectManager,description = item.description,softDeadline = item.softDeadline,hardDeadline = item.hardDeadline)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    db_resourceAssignment = resourceAssignment(projectId=db_project.id,resourceId=db_project.projectManager)
    db.add(db_resourceAssignment)
    db.commit()
    db.refresh(db_project)
    return {"message":"Project Created","data":db_project}

# complete project
@app.post("/project/complate/{id}")
def project_complated(id:uuid.UUID,db:Session=Depends(get_db)):
    db_project = db.query(project).filter(project.id == id).first()
    if not db_project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Project not found")
    db_project.endDate = datetime.now()
    db_project.isComplated = True
    db.commit()
    db_resource_assignment = db.query(resourceAssignment).where(resourceAssignment.projectId == id).all()
    for res in db_resource_assignment:
        res.offBoarding = datetime.now()
    db.commit()
    return {"message":"Project is ended"}

# Assign resources in project
@app.post("/resource/{resId}/project/{proId}",status_code=status.HTTP_202_ACCEPTED)
def add_resource_inproject(resId:uuid.UUID,proId:uuid.UUID,db:Session=Depends(get_db)):
    db_resource_assignment = resourceAssignment(projectId=proId,resourceId=resId)
    db.add(db_resource_assignment)
    db.commit()
    db.refresh(db_resource_assignment)
    return {"message":"resource added","data":db_resource_assignment}

# remove resources from project
@app.post("/remove/{resId}/{proId}",status_code=status.HTTP_200_OK)
def remove_resource_from_project(resId:uuid.UUID,proId:uuid.UUID,db:Session = Depends(get_db)):
    db_resource_assignment = db.query(resourceAssignment).filter(resourceAssignment.resourceId == resId , resourceAssignment.projectId == proId).first()
    if db_resource_assignment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Id is not exist")
    db_project = db.query(project).where(project.id == proId).one()
    if db_project.projectManager == resId:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"You can not delete manager from project you can update that")
    db_resource_assignment.offBoarding = datetime.now()
    db.commit()
    return {"message":"resource remove from project"}

# remove project manager and add new project manager
@app.post("/project/{proId}/pm/{newpmId}")
def update_pm_inproject(proId:uuid.UUID,newpmId:uuid.UUID,db:Session=Depends(get_db)):
    db_project = db.query(project).where(project.id == proId).first()
    if db_project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Project not found")
    
    db_resource_assignment = db.query(resourceAssignment).filter(resourceAssignment.resourceId == db_project.projectManager , resourceAssignment.projectId == proId).first()
    db_resource_assignment.offBoarding = datetime.now()
    add_resource_inproject(resId=newpmId,proId=proId,db=db)
    db_project.projectManager = newpmId
    db.commit()
    return {"message":"pm updated"}