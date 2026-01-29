from django.core.management.base import BaseCommand
from hello_world.core.models import WoundType, BodyPart, InsuranceProvider, MedicalScheme


class Command(BaseCommand):
    help = 'Populate wound types, body parts, and insurance data'

    def handle(self, *args, **options):
        # Create Wound Types
        wound_types = [
            {'name': 'Abrasion', 'category': 'acute', 'description': 'Scraping of skin surface'},
            {'name': 'Laceration', 'category': 'acute', 'description': 'Irregular tear in skin'},
            {'name': 'Incision', 'category': 'surgical', 'description': 'Clean surgical cut'},
            {'name': 'Puncture', 'category': 'trauma', 'description': 'Deep hole from sharp object'},
            {'name': 'Pressure Ulcer', 'category': 'ulcer', 'description': 'Bedsore from prolonged pressure'},
            {'name': 'Venous Ulcer', 'category': 'chronic', 'description': 'Ulcer from venous insufficiency'},
            {'name': 'Diabetic Ulcer', 'category': 'diabetic', 'description': 'Foot ulcer in diabetes patients'},
            {'name': 'Burn', 'category': 'burn', 'description': 'Thermal injury to skin'},
            {'name': 'Surgical Wound', 'category': 'surgical', 'description': 'Post-operative surgical site'},
            {'name': 'Dehiscence', 'category': 'surgical', 'description': 'Opening of previously closed wound'},
        ]
        
        for wt_data in wound_types:
            WoundType.objects.get_or_create(
                name=wt_data['name'],
                defaults={
                    'category': wt_data['category'],
                    'description': wt_data['description'],
                    'is_active': True,
                }
            )
        
        self.stdout.write(self.style.SUCCESS('✅ Created Wound Types'))
        
        # Create Body Parts
        body_parts = [
            # Head/Face
            {'name': 'Forehead', 'category': 'head'},
            {'name': 'Face', 'category': 'head'},
            {'name': 'Scalp', 'category': 'head'},
            {'name': 'Ear', 'category': 'head'},
            
            # Trunk
            {'name': 'Chest', 'category': 'trunk'},
            {'name': 'Abdomen', 'category': 'trunk'},
            {'name': 'Back', 'category': 'trunk'},
            {'name': 'Buttocks', 'category': 'trunk'},
            
            # Upper Limb
            {'name': 'Shoulder', 'category': 'upper_limb'},
            {'name': 'Upper Arm', 'category': 'upper_limb'},
            {'name': 'Elbow', 'category': 'upper_limb'},
            {'name': 'Forearm', 'category': 'upper_limb'},
            {'name': 'Wrist', 'category': 'upper_limb'},
            {'name': 'Hand', 'category': 'upper_limb'},
            {'name': 'Finger', 'category': 'upper_limb'},
            
            # Lower Limb
            {'name': 'Hip', 'category': 'lower_limb'},
            {'name': 'Thigh', 'category': 'lower_limb'},
            {'name': 'Knee', 'category': 'lower_limb'},
            {'name': 'Lower Leg', 'category': 'lower_limb'},
            {'name': 'Ankle', 'category': 'lower_limb'},
            {'name': 'Foot', 'category': 'lower_limb'},
            {'name': 'Toe', 'category': 'lower_limb'},
        ]
        
        for bp_data in body_parts:
            BodyPart.objects.get_or_create(
                name=bp_data['name'],
                defaults={
                    'category': bp_data['category'],
                    'is_active': True,
                }
            )
        
        self.stdout.write(self.style.SUCCESS('✅ Created Body Parts'))
        
        # Create Insurance Providers
        providers = [
            {'name': 'Jubilee Insurance', 'contact_person': 'John Kipchoge'},
            {'name': 'AAR Insurance', 'contact_person': 'Jane Mwangi'},
            {'name': 'NHIF - National Health Insurance Fund', 'contact_person': 'Government'},
            {'name': 'Britam Insurance', 'contact_person': 'Paul Kipchoge'},
            {'name': 'Amref Insurance', 'contact_person': 'Dr. Sarah Mutua'},
        ]
        
        for provider_data in providers:
            InsuranceProvider.objects.get_or_create(
                name=provider_data['name'],
                defaults={
                    'contact_person': provider_data['contact_person'],
                    'is_active': True,
                }
            )
        
        self.stdout.write(self.style.SUCCESS('✅ Created Insurance Providers'))
        
        # Create Medical Schemes for each provider
        schemes = [
            ('Jubilee Insurance', [
                {'name': 'Jubilee Standard', 'coverage_percentage': 80},
                {'name': 'Jubilee Premium', 'coverage_percentage': 95},
            ]),
            ('AAR Insurance', [
                {'name': 'AAR Basic', 'coverage_percentage': 70},
                {'name': 'AAR Comprehensive', 'coverage_percentage': 90},
            ]),
            ('NHIF - National Health Insurance Fund', [
                {'name': 'NHIF Standard', 'coverage_percentage': 60},
            ]),
            ('Britam Insurance', [
                {'name': 'Britam Health', 'coverage_percentage': 85},
                {'name': 'Britam Plus', 'coverage_percentage': 100},
            ]),
            ('Amref Insurance', [
                {'name': 'Amref Standard', 'coverage_percentage': 75},
            ]),
        ]
        
        for provider_name, scheme_list in schemes:
            provider = InsuranceProvider.objects.get(name=provider_name)
            for scheme_data in scheme_list:
                MedicalScheme.objects.get_or_create(
                    name=scheme_data['name'],
                    defaults={
                        'insurance_provider': provider,
                        'coverage_percentage': scheme_data['coverage_percentage'],
                        'is_active': True,
                    }
                )
        
        self.stdout.write(self.style.SUCCESS('✅ Created Medical Schemes'))
        self.stdout.write(self.style.SUCCESS('\n🎉 All wound care reference data populated successfully!'))
