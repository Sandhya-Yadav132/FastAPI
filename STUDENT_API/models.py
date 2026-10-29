from sqlalchemy import Column, Integer, String
from database import Base

class Student(Base):

    __tablename__ = "student_table" 

    id = Column(String(100), primary_key= True, index=True)
    name = Column(String(50))
    course = Column(String(100))
    marks = Column(Integer)
    

