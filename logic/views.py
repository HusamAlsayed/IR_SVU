from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotAllowed
# Create your views here.
from django.forms.models import model_to_dict
from .models import QuestionRecord
from django.views.decorators.csrf import csrf_exempt
import json
from .services.retrieveing import Retrieve


@csrf_exempt
def questions(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        data['question'] = data['question'].strip().lower()
        data['answer'] = data['answer'].strip().lower()
        question = QuestionRecord.objects.create(**data)
        return JsonResponse({"questions": model_to_dict(question)})
    elif request.method == "GET":
        data = list(QuestionRecord.objects.all().values())
        return JsonResponse({"questions": data})
    return HttpResponseNotAllowed({"error": "Method is not allowed!"})


@csrf_exempt
def answer_question(request):
    data = json.loads(request.body.decode('utf-8'))
    query = data['query']
    retrieve_method = data['method']
    retrieval = Retrieve()
    if retrieve_method == 'bool':
        value = retrieval.get_binary_closest_answer(query)
    elif retrieve_method == 'extend_bool':
        value = retrieval.get_extended_boolean_closest_answer(query)
    elif retrieve_method == 'vector':
        value = retrieval.get_vectorized_closest_answer(query)
    else:
        return JsonResponse({"error": "No such Method"})
    return JsonResponse({"answer": value})



english_question_list = [
    'Is the UAE and Dubai open for all tourists?',
    'Are there any movement restrictions for unvaccinated travellers in Dubai?',
    'Are there any movement restrictions for unvaccinated travellers in Dubai?',
    'What are the international travel requirements when travelling to Dubai?',
    'Do I need travel insurance when coming to Dubai?',
    'What are the procedures from my departure destination ahead of travelling to Dubai?',
    'Following arrival, what are the procedures for exiting Dubai Airports?',
    'Do I need a COVID-19 test when travelling to Dubai?',
    'Will children and newborns be subject to COVID-19 PCR tests as well?',
    'Is there going to be a mandatory quarantine for tourists?',
    'If I show symptoms on arrival at Dubai Airport and test positive, what happens?',
    'Are transit travellers required to follow the same procedures related to conducting Covid-19 PCR tests?',
    'What are the procedures when departing from Dubai?',
    'What do I need to know or what are the rules I have to follow when in Dubai?',
    'Do I have to wear a mask during my holiday in Dubai?',
    'Do tourists have to pay for the treatment and quarantine stay in a hotel if they show symptoms and/or require a second test and the test is positive?',
    'If tourists who are spending their stay at family’s, friend’s residences and show COVID-19 symptoms on arrival and require a second test, would they be required to go into quarantine?',
    'Do I need a visa and if yes, how do I apply?',
    'Are the Emirates airline flight routes fully restored?',
    'Have MICE events resumed?',
    'Have live events resumed in Dubai?',
    'Are destination weddings able to be planned in Dubai?',
    'What are the dates for Expo 2020 and where can I get further details?',
    'Do I need to be vaccinated to visit Expo 2020?',
    'Where can I find the official measures and requirements by the Dubai Government?'
]


english_answer_list = [
    '''
    'Effective from 30 August 2021, tourist visa applications are open to travellers from all countries. Depending on a passenger's nationality, they can get a visa on arrival, or apply for a pre-arranged visit visa from Dubai Immigration before travel. Please reach out to The General Directorate of Residency and Foreigners Affairs and check your country’s latest travel advisory on outbound trips.
    ''',
    '''
    Unvaccinated travellers to Dubai need to present a negative PCR test result done within the last 48 hours or a certificate of recovery from COVID-19, obtained within one month before the date of travel.
Printed or digital PCR test or vaccination certificates are accepted in English or Arabic and must include a QR code. SMS certificates are not accepted. Certificates in other languages are acceptable if they can be validated at the departure point.
Unvaccinated visitors most likely have to present the same results or certificates when attending free movement events, such as standing concerts, depending on the venue they go to.
    ''',
    '''
    Dubai is one of the world’s safest destinations –The UAE is #1globally in Bloomberg's Covid Resilience Ranking (January 2022).
The Ministry of Health and Prevention (MoHAP) alongside other relevant authorities continue to prioritise, monitor, and assure the safety and the well-being of all visitors to, and residents of Dubai as the utmost priority. Dubai Tourism continues to work diligently under the guidance from the World Health Organization to maintain rigorously high standards of public hygiene and safety, so the wellbeing of all residents and visitors remains uncompromised.
Dubai has also been recognised by the World Travel & Tourism Council (WTTC) and received its Safe Travels stamp for its safety protocols in place.
    ''',
    '''
    Effective from 26 February 2022, passengers travelling to Dubai from all countries (GCC included) must present one of the following:
A valid vaccination certificate with a QR code proving they are fully vaccinated with a vaccine approved by the WHO or the UAE
A negative PCR test with a QR code, based on a molecular diagnostic test intended for the qualitative detection of nucleic acid for SARS-COV-2 viral RNA, and issued within 48 hours from the time of sample collection to the flight time by an approved health service provider 
A valid medical certificate with a QR code issued by relevant authorities that shows they have recovered from COVID‑19 within a month prior to the date of arrival.
UAE nationals are exempt from the above, but will be required to take a PCR test on arrival at Dubai airport, unless the country of origin requires a pre-travel test.
Some passengers may require a PCR test on arrival in Dubai and they must self-quarantine until receiving a negative result. If a passenger tests positive, they should follow the guidelines issued by the Dubai Health Authority.
Children under the age of 12 and passengers with a severe or moderate disability are exempt from the PCR test.
Please check the following links for the most up-to-date requirements ahead of travelling to or transiting through Dubai: Emirates airline | FlyDubai
Printed or digital PCR or vaccination certificates are accepted in English or Arabic and must include a QR code. SMS certificates are not accepted. PCR or vaccination certificates in other languages are acceptable if they can be validated at the departure point (the date and time of the test must be detailed).
Tourists may test at any lab accredited by their health authority in their country. If you are travelling with Emirates, please click here for a list of accredited labs.
Ensure you have medical travel insurance with international coverage that covers COVID-19 before travelling.
Customers purchasing an Emirates airline or FlyDubai ticket from 1 December 2020 benefit from additional multi-risk travel insurance provided by AIG Travel or NEXtCARE through to 31 March 2022, including cover for COVID-19 and overseas medical expenses. Please see the following links for more information and a supporting FAQ: Emirates airline | FlyDubai
Fulfil entry visa requirements to visit the UAE.
Transit passengers are asked to comply with entry protocols of their final destination.
    ''',
    '''
    Yes, ensure you have medical travel insurance with international coverage that covers COVID-19 before travelling.
Customers purchasing an Emirates airline or FlyDubai ticket from 1 December 2020 benefit from additional multi-risk travel insurance provided by AIG Travel or NEXtCARE through to 31 March 2022, including cover for COVID-19 and overseas medical expenses. Please see the following links for more information and a supporting FAQ: Emirates airline | FlyDubai
    ''',
    '''
    Please check your country’s travel advisory for latest guidance on outbound trips, as well as your carrier requirements.
Fulfil entry visa requirements to visit the UAE.
    ''',
    '''
    Tourists who show symptoms on arrival and test positive for COVID-19 after being re-tested must follow the guidelines issued by the Dubai Health Authority.
The traveller will bear the cost of treatment and quarantine unless their carrier is Emirates or FlyDubai.
For those that are a COVID-19 close contact case, no quarantine is required if you are not experiencing any symptoms.
Customers purchasing an Emirates airline or FlyDubai ticket from 1 December 2020 benefit from additional multi-risk travel insurance provided by AIG Travel or NEXtCARE through to 31 March 2022, including cover for COVID-19 and overseas medical expenses. Please see the following links for more information and a supporting FAQ: Emirates airline | FlyDubai
Compliance is required with all precautionary measures in Dubai (wearing masks at public indoor venues and adhering to frequent hand sanitisation).
    ''',
    '''
    Effective from 26 February 2022, tourists and residents arriving into Dubai from any point of origin (GCC included) must present one of the following:
A valid vaccination certificate with a QR code proving they are fully vaccinated with a vaccine approved by the WHO or the UAE
A negative PCR test with a QR code, issued within 48 hours from the time of sample collection to the flight time by an approved health service provider 
A valid medical certificate with a QR code issued by relevant authorities that shows they have recovered from COVID‑19 within a month prior to the date of arrival.
Some passengers may require a PCR test on arrival in Dubai and they must self-quarantine until receiving a negative result. If a passenger tests positive, they should follow the guidelines issued by the Dubai Health Authority.
UAE nationals are exempt from the above, but will be required to take a PCR test on arrival at Dubai airport, unless the country of origin requires a pre-travel test.
Printed or digital PCR or vaccination certificates are accepted in English or Arabic and must include a QR code. SMS certificates are not accepted. PCR or vaccination certificates in other languages are acceptable if they can be validated at the departure point (the date and time of the test must be detailed).
Tourists may test at any lab accredited by their health authority in their country. If you are travelling with Emirates, please click here for a list of accredited labs.
    ''',
    '''
    All children below 12 years of age are exempt from the COVID-19 PCR test.

    ''',
    '''
    No, only if they test positive with COVID-19.
Please check carrier and Dubai travel requirements for COVID-19 PCR testing.
Passengers who need to get a COVID-19 PCR test done at arrival in Dubai should self-quarantine until they receive their results, which is expected within 12 hours.
    ''',
    '''
    If the result is positive, compliance with 10-day isolation becomes mandatory.

A person who is infected with COVID-19 will remain in isolation for a duration of 10 days (home or facility). The isolation ends after completing the 10 days with improvement in symptoms and no fever for at least three consecutive days, without any fever reduction medication.
For more information, please visit this Dubai Health Authority page.
For those that are a COVID-19 close contact case, no quarantine is required if you are not experiencing any symptoms.
    ''',
    '''
    For transit passengers, the rules and conditions for entry at the final destination will apply.
Passengers must check their country’s travel advisory for latest guidance on outbound trips, as well as the carrier requirements.
    ''',
    '''
    Passengers departing Dubai Airports will need to do a PCR test only if it is mandated by the country they are travelling to.
A rapid PCR or Rapid Antigen test will be available at the airport to travellers departing from Dubai if their destination country requires it. 
Passengers are advised to check the travel protocols of their carrier and arrival destination.
Note: Airlines have the right to deny travellers if they display any symptoms of COVID-19.
    ''',
    '''
    Responsibilities of travellers:

Adhere to all official measures and requirements established by the Dubai Government and other countries before travelling and after returning to Dubai.
Disclose any symptoms before travelling by filling in the form provided by airlines.
Tourists will bear the costs of examination and treatment abroad, in the event they are infected with COVID-19, so are advised to have international health insurance coverage that covers COVID-19 before travelling.
Take precautionary measures and self-monitor for any symptoms of COVID-19
Follow the isolation guidelines in the case you show symptoms on arrival and the result is “positive”.
    ''',
    '''
    Masks are compulsory in public indoor venues, while wearing one in outdoor areas is optional.
Additionally, you must continue to sanitise your hands frequently.
    ''',
    '''
    The traveller will bear the cost of treatment and quarantine.
Customers purchasing an Emirates airline or FlyDubai ticket from 1 December 2020 benefit from additional multi-risk travel insurance provided by AIG Travel or NEXtCARE through to 31 March 2022, including cover for COVID-19 and overseas medical expenses. Please see the following links for more information and a supporting FAQ: Emirates airline | FlyDubai
Alternatives for isolation include institutional quarantine (dedicated hotels/facilities), home or hospitalisation and potential options based on the patient’s assessment.
A person who is infected with COVID-19 will remain in isolation for 10 days (home or facility). The isolation ends after completing the 10 days with improvement in symptoms and no fever for at least three consecutive days, without any fever reduction medication.
For more information, please visit this Dubai Health Authority page.
For those that are a COVID-19 close contact case, no quarantine is required if you are not experiencing any symptoms.
The traveller will bear the cost of treatment and quarantine unless their carrier is Emirates airline or FlyDubai.
    ''',
    '''
    If the COVID-19 test result is positive, the traveller is required to adhere to the isolation guidelines. The location for isolation will be determined according to the household situation and the health status of the patient (institutional isolation or at the hospital).
A person who is infected with COVID-19 will self isolate. The isolation period for a confirmed COVID-19 case is 10 days. The isolation ends after completing the 10 days with improvement in symptoms and no fever for 3 consecutive days at least, without any fever reduction medication.
For more information, please visit this Dubai Health Authority page.
For those that are a COVID-19 close contact case, no quarantine is required if you are not experiencing any symptoms.
    ''',
    '''
    For all the visa related information please reach out to The General Directorate of Residency and Foreigners Affairs and check your country’s travel advisory for latest guidance on outbound trips.

    ''',
    '''
    Please click here for information on which destinations Emirates is flying to and from.
    ''',
    '''
    Yes, local and international MICE events have resumed as well as leisure & retail events.
All events are following stringent safety and security protocols.
Business events can operate at a reduced capacity of 70% while adhering to all government-issued protocols.
Institutional events and award ceremonies can take place with a maximum of 1,000 people, with no mandatory vaccination requirements.
    ''',
    '''
    Entertainment activities including classical, theatrical and comedy events can resume upon securing a permit, with event organisers and attendees adhering to the latest safety and precautionary measures. For more information please contact the Dubai Tourism Call Centre Tel: 600 555 559.
Mass, entertainment, sporting and business events (including audiences) must adhere to an event capacity of 70% and must follow social distancing guidelines. 
Social activities can increase capacity to 60% and not exceed 300 people. 
For event vaccination requirements, please refer to latest published protocols.
    ''',
    '''
    Yes, weddings can be planned and hosted in Dubai with an increased capacity to 60%, not exceeding 300 attendees. Elderly people and those with chronic conditions are advised not to attend gatherings.

    ''',
    '''
    The global mega event launched on 1 October and will run through to 31 March 2022. For the latest updates please visit https://www.expo2020dubai.com/ or @Expo2020dubai on social media.
    ''',
    '''
    All visitors must show proof of at least one dose of any COVID-19 vaccine, recognised by any Expo 2020 participating country or the World Health Organisation (WHO).
If unvaccinated, visitors must present a negative PCR test certificate for a test conducted within the last 72 hours.
For further information on Expo 2020’s COVID-19 safety measures, please click here.
    ''',
    '''
    The public are required to follow precautionary measures, which include:

Wearing a face mask in all public indoor venues.
Adhering to frequent hand sanitisation.
Please find below helpful links to official sources:

Dubai Airports website
Dubai Municipality website
Dubai Health Authority website
Federal Authority for Identity and Citizenship website
General Directorate of Residency and Foreigners Affairs-Dubai website
United Arab Emirates Ministry of Health & Prevention website
    '''
]


def seeder(request):
    for question, answer in zip(english_question_list, english_answer_list):
        QuestionRecord.objects.create(**{'question': question, 'answer': answer, 'base': 1})
    return JsonResponse({"Done": "YES"})