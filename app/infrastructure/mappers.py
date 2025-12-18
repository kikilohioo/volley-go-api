# app/infrastructure/mapper.py

# Mapper functions entre SQLAlchemy models y domain entities generico
# perdemos desacoplamiento pero ganamos simplicidad

from app.domain.championship.entities import Championship
from app.domain.championship.value_objects import ChampionshipName, ChampionshipStatus, ChampionshipType
from app.domain.team.entities import Team
from app.domain.user.entities import User
from app.domain.user.value_objects import UserEmail, UserPassword, UserRole


def to_domain(obj, domain_class):
    data = {}

    for field in domain_class.__dataclass_fields__.keys():
        if hasattr(obj, field):
            raw_value = getattr(obj, field)

            # TODO: mejorar este bloque con reflection o una estrategia de mapeo
            '''
            ##### User ####
            '''            
            if domain_class is User:
                # mapping para value objects
                if field == "email":
                    raw_value = UserEmail(raw_value)
                elif field == "password":
                    raw_value = UserPassword(raw_value)
                elif field == "role":
                    raw_value = UserRole(raw_value)
            '''
            ##### Championship ####
            '''    
            if domain_class is Championship:
                # Conversiones para Value Objects:
                if field == 'teams':
                    continue
                if field == "organizer":
                    raw_value = to_domain(raw_value, User)
                elif field == "name":
                    raw_value = ChampionshipName(raw_value)
                elif field == "type":
                    raw_value = ChampionshipType(raw_value)
                elif field == "status":
                    raw_value = ChampionshipStatus(raw_value)
                    
            if domain_class is Team:
                if field == 'user':
                    raw_value = to_domain(raw_value, User)

            data[field] = raw_value

    return domain_class(**data)


def to_model(domain_obj, model_class):
    data = {}

    for field, value in domain_obj.__dict__.items():
        if hasattr(value, "value"):   # es un value object
            data[field] = value.value
        else:
            if field == 'teams':
                continue
            if field == 'user':
                continue
            if field == 'organizer':
                continue
            data[field] = value

    return model_class(**data)
