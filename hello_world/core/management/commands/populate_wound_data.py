from django.core.management.base import BaseCommand
from hello_world.core.models import (
    WoundType, BodyPart, InsuranceProvider, MedicalScheme, CorporatePaymentScheme
)


class Command(BaseCommand):
    help = 'Populate wound types, body parts, insurance data, and corporate payment schemes'

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
        
        # Create Corporate Payment Schemes for Kenya
        corporate_schemes = [
            {
                'name': 'Kenya Revenue Authority (KRA) Scheme',
                'employer': 'NHIF - National Health Insurance Fund',
                'coverage_percentage': 85,
                'payment_frequency': 'monthly',
                'primary_contact_name': 'KRA HR Director',
                'primary_contact_phone': '+254722123456',
                'billing_contact_name': 'KRA Finance Officer',
                'billing_contact_phone': '+254722654321',
                'bank_name': 'KCB Bank Kenya',
                'bank_account_number': '0012345678901',
                'bank_branch': 'Nairobi HQ',
            },
            {
                'name': 'Kenya Power & Lighting Company',
                'employer': 'Jubilee Insurance',
                'coverage_percentage': 90,
                'payment_frequency': 'monthly',
                'primary_contact_name': 'KPLC HR Manager',
                'primary_contact_phone': '+254701234567',
                'billing_contact_name': 'KPLC Finance',
                'billing_contact_phone': '+254701987654',
                'bank_name': 'Equity Bank Kenya',
                'bank_account_number': '0098765432109',
                'bank_branch': 'Westlands',
            },
            {
                'name': 'Central Bank of Kenya',
                'employer': 'AAR Insurance',
                'coverage_percentage': 100,
                'payment_frequency': 'monthly',
                'primary_contact_name': 'CBK HR',
                'primary_contact_phone': '+254722111111',
                'billing_contact_name': 'CBK Finance',
                'billing_contact_phone': '+254722222222',
                'bank_name': 'Co-op Bank',
                'bank_account_number': '01234567890',
                'bank_branch': 'Upper Hill',
            },
            {
                'name': 'University of Nairobi Staff',
                'employer': 'Britam Insurance',
                'coverage_percentage': 80,
                'payment_frequency': 'monthly',
                'primary_contact_name': 'UoN HR',
                'primary_contact_phone': '+254713333333',
                'billing_contact_name': 'UoN Finance',
                'billing_contact_phone': '+254713444444',
                'bank_name': 'KCB Bank Kenya',
                'bank_account_number': '1122334455667',
                'bank_branch': 'Nairobi',
            },
            {
                'name': 'Kenya National Library Service',
                'employer': 'Amref Insurance',
                'coverage_percentage': 75,
                'payment_frequency': 'biweekly',
                'primary_contact_name': 'KNLS HR',
                'primary_contact_phone': '+254721555555',
                'billing_contact_name': 'KNLS Finance',
                'billing_contact_phone': '+254721666666',
                'bank_name': 'Equity Bank Kenya',
                'bank_account_number': '9988776655443',
                'bank_branch': 'CBD',
            },
        ]
        
        for scheme_data in corporate_schemes:
            employer_name = scheme_data.pop('employer')
            employer = InsuranceProvider.objects.get(name=employer_name)
            
            CorporatePaymentScheme.objects.get_or_create(
                name=scheme_data['name'],
                defaults={
                    'employer': employer,
                    'coverage_percentage': scheme_data['coverage_percentage'],
                    'payment_frequency': scheme_data['payment_frequency'],
                    'primary_contact_name': scheme_data.get('primary_contact_name', ''),
                    'primary_contact_phone': scheme_data.get('primary_contact_phone', ''),
                    'billing_contact_name': scheme_data.get('billing_contact_name', ''),
                    'billing_contact_phone': scheme_data.get('billing_contact_phone', ''),
                    'bank_name': scheme_data.get('bank_name', ''),
                    'bank_account_number': scheme_data.get('bank_account_number', ''),
                    'bank_branch': scheme_data.get('bank_branch', ''),
                    'status': 'active',
                }
            )
        
        self.stdout.write(self.style.SUCCESS('✅ Created Corporate Payment Schemes'))
        self.stdout.write(self.style.SUCCESS('\n🎉 All Kenya-specific billing data populated successfully!'))
