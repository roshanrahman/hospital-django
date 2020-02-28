from users.models import UserProfile
from hospital.models import Hospital
from specializations.models import Specialization


def search_results(query):
    doctors = UserProfile.objects.filter(
        first_name__icontains=query) | UserProfile.objects.filter(
            last_name__icontains=query)
    doctors = doctors.filter(
        user_type='doctor', account_status='active')
    hospitals = Hospital.objects.filter(
        name__icontains=query, status='active')
    specializations = Specialization.objects.filter(name__icontains=query)
    results = []
    for doctor in doctors:
        results.append({
            'id': doctor.id,
            'name': f'Dr. {doctor.first_name} {doctor.last_name}',
            'specialization': doctor.specialization.name if doctor.specialization is not None else 'not found',
            'type': 'doctor'
        })
    for hospital in hospitals:
        results.append({
            'id': hospital.id,
            'name': hospital.name,
            'address': hospital.address,
            'type': 'hospital'
        })
    for spec in specializations:
        results.append({
            'id': spec.id,
            'name': spec.name,
            'type': 'specialization'
        })
    return results


def get_hospital_json(hospital, only=None):
    hospital_json = {
        'hospital_id': hospital.id,
        'hospital_name': hospital.name,
        'session_duration': hospital.session_duration,
        'address': hospital.address,
        'opening_hours': hospital.opening_hours,
        'closing_hours': hospital.closing_hours,
        'contact': hospital.contact,
    }
    doctors_json = []
    for doctor in hospital.doctors.filter(account_status='active'):
        if(only is not None and not doctor.specialization.id == only):
            continue
        doctors_json.append({
            'id': doctor.id,
            'first_name': doctor.first_name,
            'last_name': doctor.last_name,
            'specialization_name': doctor.specialization.name if doctor.specialization else None,
            'specialization_id': doctor.specialization.id if doctor.specialization else None,
        })
    hospital_json['doctors'] = doctors_json
    spec_json = []
    for specialization in hospital.specialization.all():
        spec_json.append({
            'id': specialization.id,
            'name': specialization.name,
            'description': specialization.description
        })
    hospital_json['specializations'] = spec_json
    return hospital_json


def get_doctor_json(doctor):
    doctor_json = {
        'id': doctor.id,
        'first_name': doctor.first_name,
        'last_name': doctor.last_name,
        'specialization_name': doctor.specialization.name,
        'specialization_id': doctor.specialization.id,

    }
    hospitals = Hospital.objects.filter(doctors=doctor.id, status='active')
    hospitals_json = []
    for hospital in hospitals:
        hospitals_json.append({
            'hospital_id': hospital.id,
            'hospital_name': hospital.name,
            'session_duration': hospital.session_duration,
            'address': hospital.address,
            'opening_hours': hospital.opening_hours,
            'closing_hours': hospital.closing_hours,
            'contact': hospital.contact,
        })
    doctor_json['hospitals'] = hospitals_json
    return doctor_json


def get_data(query, obj_type):
    print('The query', query, obj_type)
    if(not query or not obj_type):
        return {
            'error': 'Please provide the parameters properly. query => the id of the object, obj_type => the type of object'
        }
    if(obj_type == 'doctor'):
        try:
            doctor = UserProfile.objects.get(pk=int(query))
            return get_doctor_json(doctor)

        except Exception as a:
            print(str(a))
            return {
                'error': f'No doctor found for id = {query} of type {obj_type}'
            }
    elif(obj_type == 'hospital'):
        try:
            hospital = Hospital.objects.get(pk=int(query))
            return get_hospital_json(hospital)
        except Exception as e:
            print(str(e))
            return {
                'error': f'No hospital found for id = {query} of type {obj_type}'
            }
    elif(obj_type == 'specialization'):
        try:
            specialization = Specialization.objects.get(pk=int(query))
            hospitals = Hospital.objects.filter(
                specialization=int(query), status='active')
            spec_json = {
                'id': specialization.id,
                'name': specialization.name,
                'description': specialization.description
            }
            hospitals_json = []
            for hospital in hospitals:
                hospitals_json.append(get_hospital_json(
                    hospital, only=specialization.id))
            spec_json['hospitals'] = hospitals_json
            print(spec_json)
            return spec_json
        except Exception as e:
            print(str(e))
            return {
                'error': f'No hospital found for id = {query} of type {obj_type}'
            }
