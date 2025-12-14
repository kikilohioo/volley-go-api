# app/application/mapper.py

# Mapper functions entre Request/Response models y domain entities generico
# perdemos desacoplamiento pero ganamos simplicidad

from app.api.user.schemas import UserResponse
from app.domain.championship.entities import Championship
from app.domain.championship.value_objects import ChampionshipName, ChampionshipStatus, ChampionshipType
from app.domain.user.entities import User
from app.domain.user.value_objects import UserEmail, UserPassword, UserRole


def to_domain(obj, domain_class, partial=False):
    data = {}

    for field in domain_class.__dataclass_fields__.keys():
        if hasattr(obj, field):
            raw_value = getattr(obj, field)

            # TODO: mejorar este bloque con reflection o una estrategia de mapeo
            if partial and raw_value is None:
                continue
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
                if field == "name":
                    raw_value = ChampionshipName(raw_value)
                elif field == "type":
                    raw_value = ChampionshipType(raw_value)
                elif field == "status":
                    raw_value = ChampionshipStatus(raw_value)

            data[field] = raw_value
            
    if partial:
        return data  # NO construir el domain completo

    return domain_class(**data)


def to_schema(domain_obj, schema_class):
    data = {}

    for field, value in domain_obj.__dict__.items():

        # Saltar relaciones que no querés devolver
        if field == 'teams':
            continue

        # Value Object
        if hasattr(value, "value"):
            data[field] = value.value
            continue

        # Sub-entidad (organizer, por ejemplo)
        if hasattr(value, "__dict__"):
            # ejemplo: Organizer -> UserResponse
            schema_field = schema_class.model_fields.get(field)

            if schema_field and hasattr(schema_field.annotation, "__fields__"):
                # schema_field.annotation es UserResponse
                nested_schema = schema_field.annotation
                data[field] = to_schema(value, nested_schema)
            else:
                data[field] = value

            continue

        # Primitivo
        data[field] = value

    return schema_class(**data)
