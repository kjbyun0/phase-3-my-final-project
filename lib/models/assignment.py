from models.__init__ import CURSOR, CONN
from models.course import Course
from datetime import datetime

class Assignment:
    all = {}

    def __init__(self, name, desc, due_date, course_id, id=None):
        self.id = id
        self.name = name
        self.desc = desc
        self.due_date = due_date
        self.course_id = course_id
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if isinstance(name, str) and len(name):
            self._name = name
        else:
            raise ValueError('Name must be a non-empty string')
    
    @property
    def desc(self):
        return self._desc
    
    @desc.setter
    def desc(self, desc):
        if isinstance(desc, str) and len(desc):
            self._desc = desc
        else:
            raise ValueError('Desc must be a non-empty string')
    
    @property
    def due_date(self):
        return self._due_date
    
    @due_date.setter
    def due_date(self, due_date):
        try:
            dt_due_date = datetime.strptime(due_date, "%m-%d-%Y")
            self._due_date = f'{dt_due_date.month}-{dt_due_date.day}-{dt_due_date.year}'
        except Exception as exc:
            raise ValueError("due_date must be a string in '%m-%d-%Y' format")

    @property
    def course_id(self):
        return self._course_id
    
    @course_id.setter
    def course_id(self, course_id):
        if isinstance(course_id, int) and Course.find_by_id(course_id):
            self._course_id = course_id
        else:
            raise ValueError('course_id must reference a course in the database')
        
    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS assignments (
                id INTEGER PRIMARY KEY,
                name TEXT,
                desc TEXT,
                due_date TEXT,
                course_id INTEGER,
                FOREIGN KEY (course_id) REFERENCES courses (id)
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS assignments
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        sql = """
            INSERT INTO assignments (name, desc, due_date, course_id)
            VALUES (?, ?, ?, ?)
        """
        CURSOR.execute(sql, (self.name, self.desc, self.due_date, self.course_id))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, name, desc, due_date, course_id):
        assignment = cls(name, desc, due_date, course_id)
        assignment.save()
        return assignment
    
    def update(self):
        sql = """
            UPDATE assignments 
            SET name = ?, desc = ?, due_date = ?, course_id = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.desc, self.due_date, self.course_id, self.id))
        CONN.commit()
    
    def delete(self):
        sql = """
            DELETE FROM assignments
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        
        del type(self).all[self.id]
        self.id = None

    @classmethod
    def instance_from_db(cls, row):
        assignment = cls.all.get(row[0])
        if assignment:
            assignment.name = row[1]
            assignment.desc = row[2]
            assignment.due_date = row[3]
            assignment.course_id = row[4]
        else:
            assignment = cls(row[1], row[2], row[3], row[4])
            assignment.id = row[0]
            cls.all[assignment.id] = assignment
        return assignment
    
    @classmethod
    def get_all(cls):
        sql = """
            SELECT *
            FROM assignments
        """
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT *
            FROM assignments
            WHERE id = ?
        """
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None
    
    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT *
            FROM assignments
            WHERE name = ?
        """
        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None
    