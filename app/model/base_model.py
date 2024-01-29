from sqlalchemy.ext.declarative import declarative_base

from app.db import db

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    def before_save(self, *args, **kwargs):
        pass

    def after_save(self, *args, **kwargs):
        pass

    def save(self, commit=True):
        self.before_save()
        db.session.add(self)
        if commit:
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise e
        self.after_save()

    def before_update(self, *args, **kwargs):
        pass

    def after_update(self, *args, **kwargs):
        pass

    def update(self, *args, **kwargs):
        self.before_update(*args, **kwargs)
        self.save()
        self.after_update(*args, **kwargs)

    def delete(self, commit=True):
        db.session.delete(self)
        if commit:
            db.session.commit()

    @classmethod
    def before_bulk_create(cls, iterable, *args, **kwargs):
        pass

    @classmethod
    def after_bulk_create(cls, model_objs, *args, **kwargs):
        pass

    @classmethod
    def bulk_create(cls, iterable, *args, **kwargs):
        cls.before_bulk_create(iterable, *args, **kwargs)
        model_objs = []
        for data in iterable:
            if not isinstance(data, cls):
                data = cls(**data)
            model_objs.append(data)
        db.session.bulk_save_objects(model_objs)
        if kwargs.get('commit', True) is True:
            db.session.commit()
        cls.after_bulk_create(model_objs, *args, **kwargs)
        return model_objs

    @classmethod
    def bulk_create_or_none(cls, iterable, *args, **kwargs):
        try:
            return cls.bulk_create(iterable, *args, **kwargs)
        except exc.IntegrityError as e:
            db.session.rollback()
            return None

    @classmethod
    def query(cls):
        return db.session.query(cls)
