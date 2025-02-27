from database import Base
# from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column,String,TIMESTAMP,Boolean,text,UUID,ForeignKey
import uuid

class resource(Base):
    __tablename__="resource"

    id = Column(UUID,default = uuid.uuid4(),primary_key=True)
    name = Column(String,nullable=False)
    email = Column(String,nullable=False,unique=True)
    isActive = Column(Boolean,default=True)
    createdAt = Column(TIMESTAMP(),server_default=text('now()'))
    deletedAt = Column(TIMESTAMP)

    def toDict(self):
        return {
            "id":self.id,
            "name":self.name
        }


class project(Base): # add the status in this 
    __tablename__ = "project"

    id = Column(UUID,default = uuid.uuid4(),primary_key=True)
    projectManager = Column(UUID,ForeignKey('resource.id'),nullable=False)
    name = Column(String,nullable=False,unique=True)
    description = Column(String)
    startDate = Column(TIMESTAMP(),server_default=text('now()'))
    endDate = Column(TIMESTAMP)
    softDeadline = Column(TIMESTAMP)
    hardDeadline = Column(TIMESTAMP)
    isComplated = Column(Boolean,insert_default=False)

class resourceAssignment(Base):
    __tablename__ = "resourceAssignment"

    id = Column(UUID,default = uuid.uuid4(),primary_key=True)
    projectId = Column(UUID,ForeignKey('project.id'),nullable=False)
    resourceId = Column(UUID,ForeignKey('resource.id'),nullable=False)
    onBoarding =  Column(TIMESTAMP(),server_default=text('now()'))   
    offBoarding = Column(TIMESTAMP())

