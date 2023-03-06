from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    DB = "test_db"
    def __init__(self, data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    # CRUD METHODS
    
    #CREATE
    @classmethod
    def save(cls, data):
        query = """
                INSERT INTO users 
                ( first_name , last_name , email , created_at, updated_at ) 
                VALUES 
                ( %(first_name)s , %(last_name)s , %(email)s , NOW() , NOW() )
                ;"""
        return connectToMySQL(cls.DB).query_db( query, data )
    
    
    #READ 
    @classmethod
    def get_all(cls):
        query = """
                SELECT * 
                FROM users
                ;"""
        results = connectToMySQL(cls.DB).query_db(query)
        
        users = []
        for row in results:
            users.append(cls(row))
        return users

    @classmethod 
    def get_one(cls, data):
        query = """
                SELECT * 
                FROM users 
                WHERE id = %(id)s
                ;"""
        results = connectToMySQL(cls.DB).query_db( query, data)
        return cls(results[0])
    
    
    #UPDATE
    @classmethod
    def update(cls, data):
        query = """
                UPDATE users 
                SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, updated_at = NOW() 
                WHERE id = %(id)s;
                """
        results = connectToMySQL(cls.DB).query_db(query, data)
        
        return results
    
    #DELETE
    @classmethod
    def delete(cls, data):
        query = """
                DELETE FROM users
                WHERE id = %(id)s;
                """
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results
    
    #VALIDATION 
    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters")
            is_valid = False
        if len(user['email']) < 8:
            flash("Please enter a valid email address")
            is_valid = False 
        if not EMAIL_REGEX.match(user['email']):
            flash('Invalid email address', 'email')
            is_valid = False
        return is_valid
            
    
    