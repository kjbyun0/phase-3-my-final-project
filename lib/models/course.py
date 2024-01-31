from models.__init__ import CONN, CURSOR

class Course:
    all = {}

    def __init__(self, name, desc, credit, semester, id=None):
        self.id = id
        self.name = name
        self.desc = desc
        self.credit = credit
        self.semester = semester

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if isinstance(name, str) and len(name):
            self._name = name
        else:
            raise ValueError('Course name must be a non-empty string.') 
    
    @property
    def desc(self):
        return self._desc
    
    @desc.setter
    def desc(self, desc):
        if isinstance(desc, str) and len(desc):
            self._desc = desc
        else:
            raise ValueError('Course desc must be a non-empty string')
    
    @property
    def credit(self):
        return self._credit

    @credit.setter
    def credit(self, credit):
        if isinstance(credit, float) and 0.0 < credit <= 4.0:
            self._credit = credit
        else:
            raise ValueError('Course credit must be greater than 0.0 and less than or equal to 4.0')
        
    @property
    def semester(self):
        return self._semester

    @semester.setter
    def semester(self, semester):
        if isinstance(semester, str) and \
            semester[:-5].title() in ('Spring', 'Summer', 'Fall') and \
            semester[-4:].isnumeric():
            self._semester = semester.title()       #bkj - check it
        else:
            raise ValueError("Course's semester must be in 'season year' format")
    
    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY,
                name TEXT,
                desc TEXT,
                credit REAL,
                semester TEXT
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS courses
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        sql = """
            INSERT INTO courses (name, desc, credit, semester)
            VALUES (?, ?, ?, ?) 
        """
        CURSOR.execute(sql, (self.name, self.desc, self.credit, self.semester))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, name, desc, credit, semester):
        course = cls(name, desc, credit, semester)
        course.save()
        return course
    
    def update(self):
        sql = """
            UPDATE courses
            SET name = ?, desc = ?, credit = ?, semester = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.desc, self.credit, self.semester, self.id))
        CONN.commit()

    def delete(self):
        sql = """
            DELETE FROM courses
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        del type(self).all[self.id]
        self.id = None

    @classmethod
    def instance_from_db(cls, row):
        course = cls.all.get(row[0])
        if course:
            course.name = row[1]
            course.desc = row[2]
            course.credit = row[3]
            course.semester = row[4]            
        else:
            course = cls(row[1], row[2], row[3], row[4])
            course.id = row[0]
            cls.all[course.id] = course
        return course

    @classmethod
    def get_all(cls):
        sql = """
            SELECT *
            FROM courses
        """
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]
    
    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT *
            FROM courses
            WHERE id = ?
        """

        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None
    
    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT *
            FROM courses
            WHERE name is ?
        """

        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None
    
    def assignments(self):
        from models.assignment import Assignment
        sql = """
            SELECT *
            FROM assignments
            WHERE course_id = ?
        """
        rows = CURSOR.execute(sql, (self.id,)).fetchall()
        return [Assignment.instance_from_db(row) for row in rows]
    