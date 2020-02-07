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
            'type': 'doctor'
        })
    for hospital in hospitals:
        results.append({
            'id': hospital.id,
            'name': hospital.name,
            'type': 'hospital'
        })
    for spec in specializations:
        results.append({
            'id': spec.id,
            'name': spec.name,
            'type': 'specialization'
        })
    return results
