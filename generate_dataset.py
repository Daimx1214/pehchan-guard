#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pehchan Guard - synthetic dataset generator
-------------------------------------------
Makes train / val / test JSONL files. 100% synthetic: no real person's data.
Leakage rule: every 5th item of each pool (names, areas, cities) and every
4th template is reserved for the TEST split only. Numbers are random.

Run:  python generate_dataset.py --out data --train 3200 --val 400 --test 400
"""
import argparse, json, random, re, collections

SYSTEM = (
    "You are Pehchan Guard. Replace every personal detail (name, CNIC, phone, email, "
    "address, bank account/IBAN, vehicle number) in the user's text with [NAME], [CNIC], "
    "[PHONE], [EMAIL], [ADDRESS], [BANK], [VEHICLE]. Output exactly: REDACTED: then the "
    "redacted text, then FOUND: then a list of '- TYPE: original text'. If there is no "
    "personal detail, copy the text unchanged and write '- none'."
)

# ---------------------------------------------------------------- word pools
# (roman, urdu) pairs. Lists expanded per the build guide targets:
# 60+ first names per gender, 50+ family names, 40+ areas, 25+ cities.
MALE = [("Ahmed","احمد"),("Ali","علی"),("Hassan","حسن"),("Usman","عثمان"),("Bilal","بلال"),
 ("Hamza","حمزہ"),("Zain","زین"),("Fahad","فہد"),("Imran","عمران"),("Kamran","کامران"),
 ("Tariq","طارق"),("Nadeem","ندیم"),("Saad","سعد"),("Faisal","فیصل"),("Asad","اسد"),
 ("Rizwan","رضوان"),("Shahid","شاہد"),("Waqas","وقاص"),("Adnan","عدنان"),("Junaid","جنید"),
 ("Salman","سلمان"),("Kashif","کاشف"),("Naveed","نوید"),("Irfan","عرفان"),("Haider","حیدر"),
 ("Danish","دانش"),("Shoaib","شعیب"),("Zubair","زبیر"),("Sohail","سہیل"),("Arslan","ارسلان"),
 ("Umar","عمر"),("Talha","طلحہ"),("Abdullah","عبداللہ"),("Ibrahim","ابراہیم"),("Yusuf","یوسف"),
 ("Haroon","ہارون"),("Adeel","عدیل"),("Asif","آصف"),("Atif","عاطف"),("Babar","بابر"),
 ("Fawad","فواد"),("Haseeb","حسیب"),("Khurram","خرم"),("Nasir","ناصر"),("Qasim","قاسم"),
 ("Sajid","ساجد"),("Tahir","طاہر"),("Umair","عمیر"),("Waqar","وقار"),("Yasir","یاسر"),
 ("Zeeshan","ذیشان"),("Khalid","خالد"),("Mansoor","منصور"),("Nabeel","نبیل"),("Rashid","راشد"),
 ("Tanveer","تنویر"),("Zahid","زاہد"),("Aamir","عامر"),("Farhan","فرحان"),("Hammad","حماد"),
 ("Jawad","جواد"),("Muneeb","منیب"),("Sameer","سمیر"),("Taimoor","تیمور"),("Usama","اسامہ"),
 ("Waleed","ولید"),("Zaid","زید"),("Anas","انس"),("Dawood","داؤد"),("Ehsan","احسان"),
 ("Furqan","فرقان"),("Shahbaz","شہباز"),("Jahangir","جہانگیر"),("Luqman","لقمان"),("Raheel","راحیل"),
 ("Burhan","برہان")]
FEMALE = [("Ayesha","عائشہ"),("Fatima","فاطمہ"),("Sana","ثناء"),("Hira","حرا"),("Maryam","مریم"),
 ("Zainab","زینب"),("Nida","ندا"),("Iqra","اقراء"),("Amna","آمنہ"),("Sadia","سعدیہ"),
 ("Rabia","رابعہ"),("Komal","کومل"),("Bushra","بشریٰ"),("Saima","صائمہ"),("Mehwish","مہوش"),
 ("Samina","ثمینہ"),("Farah","فرح"),("Noor","نور"),("Anum","انم"),("Laiba","لائبہ"),
 ("Areeba","اریبہ"),("Asma","اسماء"),("Amina","امینہ"),("Beenish","بینش"),("Farzana","فرزانہ"),
 ("Fauzia","فوزیہ"),("Ghazala","غزالہ"),("Hafsa","حفصہ"),("Hina","حنا"),("Huma","ہما"),
 ("Javaria","جویریہ"),("Kainat","کائنات"),("Khadija","خدیجہ"),("Lubna","لبنیٰ"),("Mahnoor","ماہ نور"),
 ("Maria","ماریہ"),("Nadia","نادیہ"),("Naila","نائلہ"),("Nazia","نازیہ"),("Nighat","نگہت"),
 ("Nimra","نمرہ"),("Razia","رضیہ"),("Rehana","ریحانہ"),("Rida","رضا"),("Rimsha","رمشا"),
 ("Rukhsana","رخسانہ"),("Saba","صبا"),("Sabina","صبینہ"),("Sajida","ساجدہ"),("Salma","سلمیٰ"),
 ("Sehrish","سحرش"),("Shabana","شبانہ"),("Shazia","شازیہ"),("Shehla","شہلا"),("Shireen","شیریں"),
 ("Sidra","سدرہ"),("Sonia","سونیا"),("Sumera","سمیرا"),("Tahira","طاہرہ"),("Tayyaba","طیبہ"),
 ("Tehreem","تحریم"),("Uzma","عظمیٰ"),("Wajiha","وجیہہ"),("Yasmeen","یاسمین"),("Zahra","زہرا"),
 ("Zara","زارا"),("Zoya","زویا"),("Arooj","عروج"),("Bisma","بسمہ"),("Dua","دعا"),
 ("Eman","ایمان"),("Kinza","کنزہ"),("Maham","ماہم"),("Memoona","میمونہ"),("Minahil","مناہل"),
 ("Nawal","نوال"),("Rania","رانیہ"),("Saman","سمن"),("Shifa","شفا"),("Tuba","طوبیٰ"),
 ("Warda","وردہ"),("Amber","عنبر"),("Anila","انیلہ"),("Bakhtawar","بختاور"),("Fareeha","فریحہ"),
 ("Gulnaz","گل ناز"),("Jannat","جنت"),("Laraib","لاریب")]
FAMILY = [("Khan","خان"),("Malik","ملک"),("Butt","بٹ"),("Chaudhry","چوہدری"),("Sheikh","شیخ"),
 ("Qureshi","قریشی"),("Siddiqui","صدیقی"),("Raza","رضا"),("Hussain","حسین"),("Baig","بیگ"),
 ("Mirza","مرزا"),("Shah","شاہ"),("Awan","اعوان"),("Gill","گل"),("Rana","رانا"),
 ("Bhatti","بھٹی"),("Niazi","نیازی"),("Abbasi","عباسی"),("Javed","جاوید"),("Ansari","انصاری"),
 ("Cheema","چیمہ"),("Mughal","مغل"),("Zaidi","زیدی"),("Rehman","رحمان"),("Ghani","غنی"),
 ("Syed","سید"),("Mehmood","محمود"),("Lodhi","لودھی"),("Rajput","راجپوت"),("Dar","ڈار"),
 ("Kiani","کیانی"),("Iqbal","اقبال"),("Akhtar","اختر"),("Aslam","اسلم"),("Aziz","عزیز"),
 ("Bajwa","باجوہ"),("Baloch","بلوچ"),("Farooqui","فاروقی"),("Gondal","گوندل"),("Gujjar","گجر"),
 ("Hashmi","ہاشمی"),("Jutt","جٹ"),("Khokhar","کھوکھر"),("Leghari","لغاری"),("Manzoor","منظور"),
 ("Mazari","مزاری"),("Mengal","مینگل"),("Minhas","منہاس"),("Naqvi","نقوی"),("Pasha","پاشا"),
 ("Qazi","قاضی"),("Rizvi","رضوی"),("Sabri","صابری"),("Sadiq","صادق"),("Safdar","صفدر"),
 ("Saleem","سلیم"),("Sandhu","سندھو"),("Sarwar","سرور"),("Sethi","سیٹھی"),("Shabbir","شبیر"),
 ("Shafi","شفیع"),("Sharif","شریف"),("Soomro","سومرو"),("Sultan","سلطان"),("Tarar","تارڑ"),
 ("Tiwana","ٹوانہ"),("Virk","ورک"),("Wahab","وہاب"),("Warraich","وڑائچ"),("Wattu","وٹو"),
 ("Yaqoob","یعقوب"),("Yaseen","یاسین"),("Yousaf","یوسف"),("Zafar","ظفر"),("Zahoor","ظہور"),
 ("Zaman","زمان"),("Zardari","زرداری"),("Zia","ضیاء"),("Zulfiqar","ذوالفقار"),("Usmani","عثمانی"),
 ("Toor","طور"),("Chohan","چوہان"),("Dogar","ڈوگر")]
CITY = [("Lahore","لاہور"),("Karachi","کراچی"),("Islamabad","اسلام آباد"),("Rawalpindi","راولپنڈی"),
 ("Multan","ملتان"),("Faisalabad","فیصل آباد"),("Peshawar","پشاور"),("Quetta","کوئٹہ"),
 ("Sialkot","سیالکوٹ"),("Gujranwala","گوجرانوالہ"),("Hyderabad","حیدرآباد"),("Bahawalpur","بہاولپور"),
 ("Sargodha","سرگودھا"),("Abbottabad","ایبٹ آباد"),("Sukkur","سکھر"),("Larkana","لاڑکانہ"),
 ("Sheikhupura","شیخوپورہ"),("Rahim Yar Khan","رحیم یار خان"),("Jhang","جھنگ"),("Dera Ghazi Khan","ڈیرہ غازی خان"),
 ("Gujrat","گجرات"),("Mardan","مردان"),("Kasur","قصور"),("Okara","اوکاڑہ"),
 ("Sahiwal","ساہیوال"),("Mirpur","میرپور"),("Chiniot","چنیوٹ"),("Sadiqabad","صادق آباد"),
 ("Muzaffargarh","مظفر گڑھ"),("Jhelum","جہلم"),("Hafizabad","حافظ آباد"),("Kohat","کوہاٹ"),
 ("Khanpur","خانپور"),("Gojra","گوجرہ"),("Mandi Bahauddin","منڈی بہاؤالدین"),("Pakpattan","پاکپتن"),
 ("Khairpur","خیرپور"),("Daska","ڈسکہ"),("Nowshera","نوشہرہ"),("Charsadda","چارسدہ"),
 ("Swabi","صوابی"),("Chakwal","چکوال"),("Mianwali","میانوالی"),("Attock","اٹک"),
 ("Vehari","وہاڑی"),("Wah","واہ"),("Burewala","بورے والا"),("Jacobabad","جیکب آباد"),
 ("Shikarpur","شکارپور"),("Kamalia","کمالیہ")]
AREA = [("Model Town","ماڈل ٹاؤن"),("Gulberg","گلبرگ"),("Johar Town","جوہر ٹاؤن"),("DHA Phase 5","ڈی ایچ اے فیز فائیو"),
 ("Bahria Town","بحریہ ٹاؤن"),("Satellite Town","سیٹلائٹ ٹاؤن"),("Iqbal Town","اقبال ٹاؤن"),
 ("Garden Town","گارڈن ٹاؤن"),("Shalimar Colony","شالیمار کالونی"),("Allama Iqbal Colony","علامہ اقبال کالونی"),
 ("Gulshan-e-Iqbal","گلشن اقبال"),("Nazimabad","ناظم آباد"),("G-10","جی-10"),("F-8","ایف-8"),
 ("Wapda Town","واپڈا ٹاؤن"),("Cantt","کینٹ"),("Samanabad","سمن آباد"),("Township","ٹاؤن شپ"),
 ("Clifton","کلفٹن"),("University Town","یونیورسٹی ٹاؤن"),("Gulistan-e-Johar","گلستان جوہر"),
 ("North Nazimabad","نارتھ ناظم آباد"),("PECHS","پی ای سی ایچ ایس"),("Federal B Area","فیڈرل بی ایریا"),
 ("Malir","ملیر"),("Korangi","کورنگی"),("Landhi","لانڈھی"),("Saddar","صدر"),
 ("Tariq Road","طارق روڈ"),("Bahadurabad","بہادرآباد"),("Askari 11","عسکری الیون"),("Valencia Town","ویلنشیا ٹاؤن"),
 ("Lake City","لیک سٹی"),("Faisal Town","فیصل ٹاؤن"),("Muslim Town","مسلم ٹاؤن"),("Shadbagh","شاد باغ"),
 ("Baghbanpura","باغبانپورہ"),("Mughalpura","مغلپورہ"),("Harbanspura","ہربنس پورہ"),("Shahdara","شاہدرہ"),
 ("Kot Lakhpat","کوٹ لکھپت"),("Green Town","گرین ٹاؤن"),("Sabzazar","سبزہ زار"),("PIA Society","پی آئی اے سوسائٹی"),
 ("EME Society","ای ایم ای سوسائٹی"),("Thokar Niaz Beg","ٹھوکر نیاز بیگ"),("Bahria Orchard","بحریہ آرچرڈ"),("Kahna","کہانہ"),
 ("G-9","جی-9"),("F-10","ایف-10"),("E-11","ای-11"),("H-8","ایچ-8"),
 ("I-8","آئی-8"),("Blue Area","بلیو ایریا"),("Margalla Town","مارگلہ ٹاؤن"),("Soan Garden","سوان گارڈن"),
 ("PWD Colony","پی ڈبلیو ڈی کالونی"),("Media Town","میڈیا ٹاؤن"),("Bahria Enclave","بحریہ انکلیو"),
 ("DHA Phase 2","ڈی ایچ اے فیز ٹو"),("Chaklala Scheme 3","چکلالہ اسکیم تھری"),("Gulraiz Colony","گلریز کالونی"),
 ("Morgah","مورگاہ"),("Tench Bhatta","ٹینچ بھاٹہ"),("Lalazar","لالہ زار"),("Westridge","ویسٹ رج"),
 ("Afshan Colony","افشاں کالونی"),("Dhok Syedan","ڈھوک سیداں"),("Misrial Road","مصریال روڈ")]
EMAIL_DOMAINS = ["gmail.com","yahoo.com","hotmail.com","outlook.com","office.pk","school.edu.pk","mail.com.pk"]
BANK_CODES = ["HABB","MEZN","UNIL","ALFH","MUCB","SCBL","BKIP","ASCM","NBPA","JSBL"]
PLATE_PREFIX = ["LEA","LEB","LEC","LED","LEE","LHR","RIA","RIB","ICT","AKL","BDA","FSA","MNA","GB","KHI"]
LANDLINE = ["042","021","051","061","041","091","081","052","022","055"]

def split_pool(items, k=5):
    """every k-th element -> test only (k=5 for names/places, k=4 for templates)"""
    train = [x for i, x in enumerate(items) if i % k != k - 1]
    test = [x for i, x in enumerate(items) if i % k == k - 1]
    return train, test

# ---------------------------------------------------------------- templates
# Placeholders: {NAME} {NAME2} {CNIC} {PHONE} {EMAIL} {ADDRESS} {BANK} {VEHICLE}
# Same key twice in one text = same value. {NAME} and {NAME2} = two different people.
EN = [
 "Please call {NAME} on {PHONE} regarding the appointment.",
 "Patient {NAME}, CNIC {CNIC}, was admitted today. Contact: {PHONE}.",
 "Dear Sir, my name is {NAME} and I live at {ADDRESS}. You can reach me at {EMAIL}.",
 "Kindly transfer the amount to account {BANK} in the name of {NAME}.",
 "Vehicle {VEHICLE} is registered to {NAME}, CNIC {CNIC}.",
 "Delivery for {NAME}: {ADDRESS}. The rider will call {PHONE} before arriving.",
 "Meeting moved to 3 pm. {NAME} and {NAME2} will attend from our side.",
 "I, {NAME}, son of {NAME2}, hereby apply for the post of accountant. My CNIC is {CNIC}.",
 "Student {NAME} (parent contact {PHONE}) was absent on Monday.",
 "Send the invoice to {EMAIL} and copy {NAME}.",
 "Dr. {NAME} will see you at the clinic. For changes call {PHONE} or email {EMAIL}.",
 "Complaint filed by {NAME}, resident of {ADDRESS}, phone {PHONE}.",
 "Salary will be credited to {BANK}. Employee: {NAME}, CNIC {CNIC}.",
 "The car {VEHICLE} was parked outside. Please ask the owner, {NAME}, to move it.",
 "Reference letter for {NAME}, who can be contacted at {EMAIL} or {PHONE}.",
 "Please note the new address of {NAME}: {ADDRESS}.",
 "Guarantor details: {NAME}, CNIC {CNIC}, mobile {PHONE}, address {ADDRESS}.",
 "Hi {NAME}, your parcel will arrive tomorrow. Questions? Reply to this message or call {PHONE}.",
 "Visitor log: {NAME}, vehicle {VEHICLE}, meeting with {NAME2}.",
 "Refund of the fee will be sent to {BANK}. Applicant email: {EMAIL}.",
 "Please verify the CNIC {CNIC} of {NAME} before issuing the card.",
 "Payment received from {NAME}, account {BANK}. Thank you.",
 "Admission form: candidate {NAME}, CNIC {CNIC}, contact {PHONE}, email {EMAIL}.",
 "Cheque will be issued to {NAME}; please confirm the account {BANK} and CNIC {CNIC}.",
 "The tenant, {NAME}, CNIC {CNIC}, has signed the rent agreement for {ADDRESS}.",
 "For home delivery, note the address: {ADDRESS}. Customer: {NAME}, {PHONE}.",
 "Your appointment with Dr. {NAME} is confirmed. A reminder will be sent to {PHONE}.",
 "The cheque book for account {BANK} will be delivered to {ADDRESS}.",
 "Please update the mobile number of {NAME} to {PHONE} in our records.",
 "Emergency contact: {NAME}, reachable at {PHONE} in case of any issue.",
 "The driving licence of {NAME}, CNIC {CNIC}, expires next month.",
 "Insurance claim for vehicle {VEHICLE} submitted by {NAME}. Documents were sent to {EMAIL}.",
 "The hostel warden may contact the parent of {NAME} at {PHONE} in an emergency.",
 "The electricity bill for {ADDRESS} is registered in the name of {NAME}.",
 "Court notice was served to {NAME} at {ADDRESS}. The hearing is next Tuesday.",
 "Please courier the documents to {NAME}, {ADDRESS}, and inform on {PHONE}.",
 "Bank statement for {BANK} was emailed to {EMAIL} on the request of {NAME}.",
 "SIM registration: subscriber {NAME}, CNIC {CNIC}, number {PHONE}.",
 "The scholarship amount for {NAME} will be credited to {BANK}.",
 "Workshop registration confirmed for {NAME}. Details have been sent to {EMAIL}.",
 "Gate pass issued to {NAME}, vehicle {VEHICLE}, CNIC {CNIC}.",
 "Please ask {NAME} to collect the parcel from {ADDRESS} and bring CNIC {CNIC}.",
 "Rent will be transferred to {BANK} by the 5th. Landlord: {NAME}, {PHONE}.",
 "The patient file of {NAME} lists contact {PHONE} for the family.",
 "Tuition teacher required at {ADDRESS}. Please call {NAME} on {PHONE}.",
 "Job offer letter issued to {NAME}, CNIC {CNIC}. Details have been sent to {EMAIL}.",
 "Vehicle {VEHICLE} is insured under {NAME}, CNIC {CNIC}, phone {PHONE}.",
 "Kindly book a room for {NAME} arriving on Friday. Confirmation to {EMAIL}.",
 "The lost CNIC of {NAME} was found near the gate. The owner may call {PHONE}.",
 "Donation received from {NAME} via {BANK}. Receipt sent to {EMAIL}.",
 "Please change the delivery address for the order of {NAME} to {ADDRESS}.",
 "Father name: {NAME2}. Candidate name: {NAME}. CNIC: {CNIC}.",
 "The committee approved the loan of {NAME}, account {BANK}, CNIC {CNIC}.",
 "Mobile wallet registered to {NAME}, number {PHONE}, CNIC {CNIC}.",
 "Please send the test reports of {NAME} to {EMAIL} and inform the family on {PHONE}.",
 "Security noted: {NAME}, vehicle {VEHICLE}, entered at 9:40 am to meet {NAME2}.",
 "The admission of {NAME} is confirmed against CNIC {CNIC}; the fee will be deposited in {BANK}.",
 "For any query about the plot file, contact {NAME} at {PHONE} or visit {ADDRESS}.",
 "The traffic warden fined vehicle {VEHICLE} near the signal. Owner {NAME} was informed on {PHONE}.",
 "Car lifted: {VEHICLE}, owner {NAME}, CNIC {CNIC}. Please contact the police station.",
 "Please wash and park the car {VEHICLE} of {NAME} at {ADDRESS}.",
]
EN_CLEAN = [
 "The meeting is at 3 pm tomorrow in the main conference room.",
 "Order #48213 totals Rs 5,400 and will ship on 12 December.",
 "Please submit the assignment by Friday and keep it under two pages.",
 "The clinic is closed on Sunday; regular hours resume on Monday at 9 am.",
 "Our office is located in Lahore and the branch in Karachi opens next month.",
 "Reminder: the bank will be closed on the 5th of February for the holiday.",
 "The seminar starts at 11 am and lunch will be served at 1 pm.",
 "Please bring a pen and your notebook to the workshop on Thursday.",
 "Shipping is free for orders above Rs 3,000 within the country.",
 "Ticket 7781 has been resolved. Thank you for your patience.",
 "The delivery window is between 10 am and 2 pm, Monday to Saturday.",
 "The workshop on Friday has been moved to the second floor seminar hall.",
 "Pakistan won the match by five wickets with two overs to spare.",
 "The new session begins in September and admissions close in August.",
 "Please water the plants while the office is closed for the holidays.",
 "The train arrives at platform 4 at 6:30 in the evening.",
 "Our team scored 92 percent on the last quarterly review.",
 "The recipe needs two cups of flour and half a teaspoon of salt.",
 "Winter uniforms will be available in the school shop from Monday.",
 "The library stays open until 8 pm during the exam week.",
 "Road work on the main boulevard will finish by the end of this month.",
 "The museum entry is free for students every first Sunday.",
 "Please keep the gate closed after 10 pm for security reasons.",
 "The annual dinner is planned for the last Friday of December.",
 "Flight PK-301 departs at 9:15 am; boarding starts forty minutes earlier.",
 "The committee will announce the results after the final round on Sunday.",
 "Rain is expected in the northern areas over the weekend.",
 "The course outline has twelve lectures and two class tests.",
 "Children under five enter the park free of charge.",
 "The store offers a one year warranty on all electronic items.",
 "Meeting minutes of the last session are attached for your review.",
]
RU = [
 "Assalam o Alaikum, mera naam {NAME} hai aur mera number {PHONE} hai.",
 "{NAME} sahab ka CNIC {CNIC} hai, form mein likh dein.",
 "Parcel {ADDRESS} par bhejna hai, rider {NAME} se is number par rabta kare: {PHONE}.",
 "Bhai payment {BANK} par kar do, account title {NAME} hai.",
 "Meri gari {VEHICLE} thi, mera email {EMAIL} hai.",
 "Kal subah meeting hai, {NAME} aur {NAME2} dono ko bata dena.",
 "Mujhe {NAME} ne bataya ke un ka ghar {ADDRESS} mein hai.",
 "Bachay ka naam {NAME} hai, walid ka number {PHONE}, school form ke liye CNIC {CNIC} chahiye.",
 "Hi {NAME}, aap ka order {ADDRESS} par deliver ho gaya hai, koi issue ho to call karein {PHONE}.",
 "Is gari {VEHICLE} ke malik {NAME} hain, un se rabta {PHONE} par karein.",
 "Dr. {NAME} kal clinic mein nahi hongi, appointment ke liye {PHONE} par message karein.",
 "Mera account number {BANK} hai, naam {NAME} likhna.",
 "Bhai salary slip {EMAIL} par bhej do aur {NAME} ko cc kar dena.",
 "Shikayat {NAME} ne darj ki hai, un ka pata {ADDRESS} hai aur CNIC {CNIC}.",
 "Yaar {NAME} ka number save kar lo: {PHONE}. Wo kal Lahore aa raha hai.",
 "Jazakallah, form jama kar diya hai. Mera naam {NAME} aur email {EMAIL} hai.",
 "Admission ke liye {NAME} walid {NAME2} CNIC {CNIC} address {ADDRESS} likha hai.",
 "Gari {VEHICLE} gate par khari hai, {NAME} se kahein hata lein.",
 "Aap ki refund {BANK} mein bhej di gayi hai, receipt {EMAIL} par mil jayegi.",
 "Meeting kal 3 baje hai, {NAME} sab ko {PHONE} par yaad dila dein.",
 "Kripya {NAME} ka CNIC {CNIC} check kar lein phir card issue karein.",
 "Paisay mil gaye, {NAME} ke account {BANK} se aaye hain.",
 "Admission form mein {NAME}, CNIC {CNIC}, number {PHONE} aur email {EMAIL} likhein.",
 "Cheque {NAME} ke naam banega, account {BANK} aur CNIC {CNIC} confirm kar dein.",
 "Kiraya har mahine {BANK} mein jama karwana hai, malik makan {NAME} hain, rabta {PHONE}.",
 "{NAME} ki report {EMAIL} par bhej dein aur ghar walon ko {PHONE} par bata dein.",
 "Bijli ka bill {ADDRESS} ke naam par hai, koi masla ho to {NAME} se {PHONE} par baat karein.",
 "Bhai mera CNIC gum ho gaya hai, naam {NAME} hai, mil jaye to {PHONE} par call kar dein.",
 "Gaari {VEHICLE} ki insurance {NAME} ke naam hai, CNIC {CNIC}.",
 "Parcel ka pata ghalat likha gaya hai, sahi pata ye hai: {ADDRESS}, naam {NAME}.",
 "Bank se cheque book {ADDRESS} par bhejni hai, account {BANK} hai.",
 "{NAME} sahab ki salary {BANK} mein aati hai, CNIC {CNIC} note kar lein.",
 "Mulaqat ke liye {NAME} kal aayenge, un ki gaari {VEHICLE} gate par khari hogi.",
 "School ki fee {BANK} mein jama hogi, bachay ka naam {NAME} hai.",
 "Plumber ko {ADDRESS} par bhej dein, {NAME} ko {PHONE} par pehle bata dein.",
 "Mera email ghalat likh gaya hai, sahi email {EMAIL} hai, naam {NAME}.",
 "Hostel mein kamra {NAME} ko allot hua hai, walid ka number {PHONE} hai.",
 "Doctor sahab ne {NAME} ki report {EMAIL} par mangwayi hai.",
 "SIM band karwani hai, number {PHONE} hai, naam {NAME}, CNIC {CNIC}.",
 "Shadi ka card {ADDRESS} par bhejna hai, {NAME} ke naam se.",
 "Tuition ke liye {NAME} ke ghar jana hai, pata {ADDRESS} hai.",
 "Refund abhi tak nahi aya, account {BANK} hai, naam {NAME}.",
 "Court ka notice {NAME} ko {ADDRESS} par mila hai.",
 "{NAME} ka mobile {PHONE} band mil raha hai, un ke bhai {NAME2} ko bata dein.",
 "Naya number note kar lein, {NAME} ka number ab {PHONE} hai.",
 "Dukaan ka samaan {ADDRESS} par pohanchana hai, {NAME} receive karenge, {PHONE}.",
 "Meri walida {NAME} hospital mein hain, rabta {PHONE} par karein.",
 "Form mein walid ka naam {NAME2} aur apna naam {NAME} likha hai, CNIC {CNIC}.",
 "Gaari {VEHICLE} ki file {NAME} ke paas hai, un se {PHONE} par rabta karein.",
 "Loan ki darkhwast {NAME} ne di hai, account {BANK}, CNIC {CNIC}.",
 "Bijli walon ko shikayat darj karani hai, pata {ADDRESS}, naam {NAME}, number {PHONE}.",
 "Mehman {NAME} kal aa rahe hain, un ko {PHONE} par airport ka rasta bata dein.",
 "Purana CNIC {CNIC} block kar ke naya banana hai, naam {NAME}.",
 "Office ka naya pata: {ADDRESS}. Manager {NAME}, rabta {PHONE}.",
 "Sadqa ki raqam {BANK} mein bhejni hai, {NAME} ko {EMAIL} par raseed bhej dein.",
 "Traffic police ne gaari {VEHICLE} ka challan kar diya, malik {NAME} ko {PHONE} par bata dein.",
 "Meri gaari {VEHICLE} service ke liye di hai, naam {NAME}, number {PHONE}.",
 "Gaari {VEHICLE} ka token tax {NAME} ne {BANK} se jama karwaya.",
]
RU_CLEAN = [
 "Kal subah 10 baje meeting hai, sab log time par pohanch jayein.",
 "Order number 48213 hai aur total bill Rs 5,400 bana hai.",
 "Assignment Friday tak jama kara dein, shukriya.",
 "Clinic Sunday ko band rehta hai, Monday ko subah 9 baje khulega.",
 "Hamara office Lahore mein hai aur Karachi ki branch agle mahine khulegi.",
 "Parcel kal dopahar tak pohanch jayega, intezar farmayein.",
 "Ticket 7781 hal ho gaya hai, aap ke sabr ka shukriya.",
 "Bank 5 February ko chuttion ki wajah se band rahega.",
 "Seminar 11 baje shuru hoga aur lunch 1 baje milega.",
 "Workshop mein Thursday ko apni copy aur pen saath layein.",
 "Rs 3,000 se zyada ke orders par shipping free hai.",
 "Pakistan ne match paanch wickets se jeet liya hai.",
 "Naya session September se shuru hoga aur dakhle August mein band honge.",
 "Barish ka imkaan hai, kal chhata saath rakhna.",
 "Train shaam 6:30 par platform 4 par aayegi.",
 "Library imtehan wale hafte mein raat 8 baje tak khuli rahegi.",
 "Dukaan par tamam cheezon par ek saal ki warranty hai.",
 "Bachon ke liye park mein dakhla bilkul muft hai.",
 "Course mein kul baarah lectures aur do class tests honge.",
 "Sadak ki marammat is mahine ke aakhir tak mukammal ho jayegi.",
 "Salana dinner December ke aakhri Jumma ko rakha gaya hai.",
 "Gate raat 10 baje ke baad band rakhein, ye hifazat ke liye hai.",
 "Committee final round ke baad Sunday ko nateeja sunayegi.",
 "Aakhri meeting ke minutes aap ke review ke liye saath hain.",
 "Recipe mein do cup aata aur aadha chamach namak chahiye.",
 "Sardi ki uniforms Monday se school ki dukaan par milengi.",
 "Office chhuttiyon mein band rahega, podon ko paani dete rehna.",
]
UR = [
 "میرا نام {NAME} ہے اور میرا نمبر {PHONE} ہے۔",
 "{NAME} صاحب کا شناختی کارڈ نمبر {CNIC} ہے، فارم میں لکھ دیں۔",
 "پارسل اس پتے پر بھیجنا ہے: {ADDRESS}، ڈیلیوری سے پہلے {PHONE} پر رابطہ کریں۔",
 "ادائیگی اس اکاؤنٹ میں کر دیں: {BANK}، اکاؤنٹ ہولڈر کا نام {NAME} ہے۔",
 "یہ گاڑی {VEHICLE} میری ہے، میرا ای میل {EMAIL} ہے۔",
 "کل صبح میٹنگ ہے، {NAME} اور {NAME2} دونوں کو اطلاع کر دیں۔",
 "{NAME} نے بتایا کہ ان کا گھر {ADDRESS} میں ہے۔",
 "بچے کا نام {NAME} ہے، والد کا نمبر {PHONE} ہے، اسکول فارم کے لیے شناختی کارڈ {CNIC} درکار ہے۔",
 "السلام علیکم {NAME}، آپ کا آرڈر {ADDRESS} پر پہنچا دیا گیا ہے، کوئی مسئلہ ہو تو {PHONE} پر کال کریں۔",
 "اس گاڑی {VEHICLE} کے مالک {NAME} ہیں، ان سے {PHONE} پر رابطہ کریں۔",
 "ڈاکٹر {NAME} کل کلینک میں نہیں ہوں گی، ملاقات کے لیے {PHONE} پر پیغام بھیجیں۔",
 "میرا اکاؤنٹ نمبر {BANK} ہے، نام {NAME} لکھنا ہے۔",
 "بھائی تنخواہ کی سلپ {EMAIL} پر بھیج دو اور {NAME} کو بھی شامل کر دینا۔",
 "شکایت {NAME} نے درج کرائی ہے، ان کا پتہ {ADDRESS} ہے اور شناختی کارڈ {CNIC} ہے۔",
 "{NAME} کا نمبر محفوظ کر لو: {PHONE}، وہ کل لاہور آ رہا ہے۔",
 "جزاک اللہ، فارم جمع کرا دیا ہے۔ میرا نام {NAME} اور ای میل {EMAIL} ہے۔",
 "داخلے کے لیے {NAME} ولد {NAME2}، شناختی کارڈ {CNIC}، پتہ {ADDRESS} لکھا ہے۔",
 "گاڑی {VEHICLE} گیٹ پر کھڑی ہے، {NAME} سے کہیں ہٹا لیں۔",
 "آپ کی رقم {BANK} میں بھیج دی گئی ہے، رسید {EMAIL} پر مل جائے گی۔",
 "میٹنگ کل تین بجے ہے، {NAME} سب کو {PHONE} پر یاد دلا دیں۔",
 "براہ کرم {NAME} کا شناختی کارڈ {CNIC} جانچ لیں پھر کارڈ جاری کریں۔",
 "پیسے مل گئے ہیں، {NAME} کے اکاؤنٹ {BANK} سے آئے ہیں۔",
 "داخلہ فارم میں {NAME}، شناختی کارڈ {CNIC}، نمبر {PHONE} اور ای میل {EMAIL} لکھیں۔",
 "چیک {NAME} کے نام بنے گا، اکاؤنٹ {BANK} اور شناختی کارڈ {CNIC} تصدیق کر دیں۔",
 "کرایہ ہر ماہ {BANK} میں جمع کروانا ہے، مالک مکان {NAME} ہیں، رابطہ {PHONE}۔",
 "{NAME} کی رپورٹ {EMAIL} پر بھیج دیں اور گھر والوں کو {PHONE} پر اطلاع دیں۔",
 "بجلی کا بل {ADDRESS} کے نام پر ہے، کوئی مسئلہ ہو تو {NAME} سے {PHONE} پر بات کریں۔",
 "میرا شناختی کارڈ گم ہو گیا ہے، نام {NAME} ہے، مل جائے تو {PHONE} پر کال کر دیں۔",
 "گاڑی {VEHICLE} کی انشورنس {NAME} کے نام ہے، شناختی کارڈ {CNIC}۔",
 "پارسل کا پتہ غلط لکھا گیا ہے، درست پتہ یہ ہے: {ADDRESS}، نام {NAME}۔",
 "بینک سے چیک بک {ADDRESS} پر بھیجنی ہے، اکاؤنٹ {BANK} ہے۔",
 "{NAME} صاحب کی تنخواہ {BANK} میں آتی ہے، شناختی کارڈ {CNIC} نوٹ کر لیں۔",
 "ملاقات کے لیے {NAME} کل آئیں گے، ان کی گاڑی {VEHICLE} گیٹ پر کھڑی ہوگی۔",
 "اسکول کی فیس {BANK} میں جمع ہوگی، بچے کا نام {NAME} ہے۔",
 "پلمبر کو {ADDRESS} پر بھیج دیں، {NAME} کو {PHONE} پر پہلے بتا دیں۔",
 "میرا ای میل غلط لکھا گیا ہے، درست ای میل {EMAIL} ہے، نام {NAME}۔",
 "ہاسٹل میں کمرہ {NAME} کو الاٹ ہوا ہے، والد کا نمبر {PHONE} ہے۔",
 "ڈاکٹر صاحب نے {NAME} کی رپورٹ {EMAIL} پر منگوائی ہے۔",
 "سم بند کروانی ہے، نمبر {PHONE} ہے، نام {NAME}، شناختی کارڈ {CNIC}۔",
 "شادی کا کارڈ {ADDRESS} پر بھیجنا ہے، {NAME} کے نام سے۔",
 "ٹیوشن کے لیے {NAME} کے گھر جانا ہے، پتہ {ADDRESS} ہے۔",
 "رقم ابھی تک نہیں آئی، اکاؤنٹ {BANK} ہے، نام {NAME}۔",
 "عدالت کا نوٹس {NAME} کو {ADDRESS} پر موصول ہوا ہے۔",
 "{NAME} کا موبائل {PHONE} بند مل رہا ہے، ان کے بھائی {NAME2} کو بتا دیں۔",
 "نیا نمبر نوٹ کر لیں، {NAME} کا نمبر اب {PHONE} ہے۔",
 "دکان کا سامان {ADDRESS} پر پہنچانا ہے، {NAME} وصول کریں گے، {PHONE}۔",
 "میری والدہ {NAME} اسپتال میں ہیں، رابطہ {PHONE} پر کریں۔",
 "فارم میں والد کا نام {NAME2} اور اپنا نام {NAME} لکھا ہے، شناختی کارڈ {CNIC}۔",
 "گاڑی {VEHICLE} کی فائل {NAME} کے پاس ہے، ان سے {PHONE} پر رابطہ کریں۔",
 "قرض کی درخواست {NAME} نے دی ہے، اکاؤنٹ {BANK}، شناختی کارڈ {CNIC}۔",
 "بجلی والوں کو شکایت درج کرانی ہے، پتہ {ADDRESS}، نام {NAME}، نمبر {PHONE}۔",
 "مہمان {NAME} کل آ رہے ہیں، ان کو {PHONE} پر ایئرپورٹ کا راستہ بتا دیں۔",
 "پرانا شناختی کارڈ {CNIC} بلاک کر کے نیا بنانا ہے، نام {NAME}۔",
 "دفتر کا نیا پتہ: {ADDRESS}۔ مینیجر {NAME}، رابطہ {PHONE}۔",
 "صدقے کی رقم {BANK} میں بھیجنی ہے، {NAME} کو {EMAIL} پر رسید بھیج دیں۔",
 "ٹریفک پولیس نے گاڑی {VEHICLE} کا چالان کر دیا، مالک {NAME} کو {PHONE} پر اطلاع دیں۔",
 "میری گاڑی {VEHICLE} سروس کے لیے دی ہے، نام {NAME}، نمبر {PHONE}۔",
 "گاڑی {VEHICLE} کا ٹوکن ٹیکس {NAME} نے {BANK} سے جمع کروایا۔",
]
UR_CLEAN = [
 "کل صبح دس بجے میٹنگ ہے، سب لوگ وقت پر پہنچ جائیں۔",
 "آرڈر نمبر 48213 ہے اور کل بل 5,400 روپے بنا ہے۔",
 "اسائنمنٹ جمعہ تک جمع کرا دیں، شکریہ۔",
 "کلینک اتوار کو بند رہتا ہے، پیر کو صبح نو بجے کھلے گا۔",
 "ہمارا دفتر لاہور میں ہے اور کراچی کی شاخ اگلے ماہ کھلے گی۔",
 "پارسل کل دوپہر تک پہنچ جائے گا، انتظار فرمائیں۔",
 "ٹکٹ 7781 کا مسئلہ حل ہو گیا ہے، آپ کے صبر کا شکریہ۔",
 "بینک 5 فروری کو چھٹی کی وجہ سے بند رہے گا۔",
 "سیمینار گیارہ بجے شروع ہوگا اور کھانا ایک بجے ملے گا۔",
 "ورکشاپ میں جمعرات کو اپنی کاپی اور قلم ساتھ لائیں۔",
 "3,000 روپے سے زیادہ کے آرڈر پر ڈیلیوری بالکل مفت ہے۔",
 "پاکستان نے میچ پانچ وکٹوں سے جیت لیا ہے۔",
 "نیا سیشن ستمبر سے شروع ہوگا اور داخلے اگست میں بند ہوں گے۔",
 "بارش کا امکان ہے، کل چھتری ساتھ رکھنا۔",
 "ٹرین شام 6:30 پر پلیٹ فارم چار پر آئے گی۔",
 "لائبریری امتحان والے ہفتے میں رات آٹھ بجے تک کھلی رہے گی۔",
 "دکان پر تمام چیزوں پر ایک سال کی وارنٹی ہے۔",
 "بچوں کے لیے پارک میں داخلہ بالکل مفت ہے۔",
 "کورس میں کل بارہ لیکچر اور دو کلاس ٹیسٹ ہوں گے۔",
 "سڑک کی مرمت اس ماہ کے آخر تک مکمل ہو جائے گی۔",
 "سالانہ عشائیہ دسمبر کے آخری جمعہ کو رکھا گیا ہے۔",
 "گیٹ رات دس بجے کے بعد بند رکھیں، یہ حفاظت کے لیے ہے۔",
 "کمیٹی فائنل راؤنڈ کے بعد اتوار کو نتیجہ سنائے گی۔",
 "آخری میٹنگ کے منٹس آپ کے جائزے کے لیے ساتھ ہیں۔",
 "ترکیب میں دو کپ آٹا اور آدھا چمچ نمک چاہیے۔",
 "سردی کی وردیاں پیر سے اسکول کی دکان پر ملیں گی۔",
 "دفتر چھٹیوں میں بند رہے گا، پودوں کو پانی دیتے رہنا۔",
 "میٹنگ کل سہ پہر تین بجے مرکزی کانفرنس روم میں ہے۔",
 "براہ کرم جمعہ تک اسائنمنٹ جمع کرائیں اور اسے دو صفحات سے کم رکھیں۔",
 "عجائب گھر میں طلبہ کے لیے ہر پہلے اتوار داخلہ مفت ہے۔",
]

# ---------------------------------------------------------------- value makers
class Pools:
    def __init__(self, which):
        sel = 0 if which == "train" else 1
        self.male = split_pool(MALE)[sel]
        self.female = split_pool(FEMALE)[sel]
        self.family = split_pool(FAMILY)[sel]
        self.city = split_pool(CITY)[sel]
        self.area = split_pool(AREA)[sel]
        self.en = split_pool(EN, 4)[sel]; self.en_clean = split_pool(EN_CLEAN, 4)[sel]
        self.ru = split_pool(RU, 4)[sel]; self.ru_clean = split_pool(RU_CLEAN, 4)[sel]
        self.ur = split_pool(UR, 4)[sel]; self.ur_clean = split_pool(UR_CLEAN, 4)[sel]

def digits(r, n):
    return "".join(r.choice("0123456789") for _ in range(n))

def mk_name(r, P, lang, latin_in_urdu=False):
    first = r.choice(P.male + P.female)
    fam = r.choice(P.family)
    idx = 1 if (lang == "ur" and not latin_in_urdu) else 0
    form = r.random()
    if form < 0.72: return f"{first[idx]} {fam[idx]}"
    if form < 0.92: return first[idx]
    return fam[idx] if lang != "ur" else f"{first[idx]} {fam[idx]}"

def mk_cnic(r):
    first = r.choice("1234567"); a = first + digits(r, 4)
    s = f"{a}-{digits(r,7)}-{r.choice('0123456789')}"
    return s if r.random() < 0.85 else s.replace("-", "")

def mk_phone(r):
    k = r.random()
    mob = "03" + r.choice("01234") + r.choice("0123456789")
    if k < 0.40: return f"{mob}-{digits(r,7)}"
    if k < 0.55: return f"{mob}{digits(r,7)}"
    if k < 0.65: return f"{mob} {digits(r,7)}"
    if k < 0.80: return f"+92 {mob[1:]} {digits(r,7)}"
    if k < 0.87: return f"+92-{mob[1:]}-{digits(r,7)}"
    code = r.choice(LANDLINE)
    return f"{code}-{digits(r,8)}" if code in ("042","021","051") else f"{code}-{digits(r,7)}"

def mk_email(r, P):
    f = r.choice(P.male + P.female)[0].lower(); l = r.choice(P.family)[0].lower()
    style = r.random()
    local = f"{f}.{l}" if style < 0.4 else f"{f}_{l}{digits(r,2)}" if style < 0.7 else f"{f}{l}{r.randint(1,99)}"
    return f"{local}@{r.choice(EMAIL_DOMAINS)}"

def iban_pk(r):
    bban = r.choice(BANK_CODES) + digits(r, 16)
    tmp = bban + "PK00"
    num = "".join(str(int(c, 36)) for c in tmp)
    check = 98 - int(num) % 97
    return f"PK{check:02d}{bban}"

def mk_bank(r):
    k = r.random()
    if k < 0.60:
        s = iban_pk(r)
        return s if r.random() < 0.5 else " ".join(s[i:i+4] for i in range(0, len(s), 4))
    if k < 0.85: return digits(r, r.choice([10, 12, 13, 14]))
    return f"{digits(r,4)}-{digits(r,10)}"

def mk_vehicle(r):
    p = r.choice(PLATE_PREFIX); k = r.random()
    if k < 0.55: return f"{p}-{r.randint(100,9999)}"
    if k < 0.80: return f"{p}-{r.randint(10,24)}-{r.randint(100,9999)}"
    if k < 0.90: return f"{p} {r.randint(100,9999)}"
    return f"{p}{r.randint(100,9999)}"

def mk_address(r, P, lang):
    n = r.randint(1, 450); s = r.randint(1, 60)
    area, city = r.choice(P.area), r.choice(P.city)
    blk = r.choice("ABCDEFGH")
    if lang == "ur":
        return r.choice([
            f"مکان نمبر {n}، گلی نمبر {s}، {area[1]}، {city[1]}",
            f"مکان نمبر {n}، {area[1]}، {city[1]}",
            f"فلیٹ نمبر {n}، بلاک {blk}، {area[1]}، {city[1]}"])
    en = [f"House {n}, Street {s}, {area[0]}, {city[0]}", f"H# {n}, St {s}, {area[0]}, {city[0]}",
          f"Flat {n}, Block {blk}, {area[0]}, {city[0]}", f"{n}-{blk}, {area[0]}, {city[0]}",
          f"House No. {n}, {area[0]}, {city[0]}"]
    ru = [f"ghar number {n}, gali {s}, mohalla {area[0]}, {city[0]}", f"makan {n}, {area[0]}, {city[0]}",
          f"ghar {n} street {s} {area[0]} {city[0]}"]
    return r.choice(en if lang == "en" else en + ru)

LABEL = {"NAME":"NAME","NAME2":"NAME","CNIC":"CNIC","PHONE":"PHONE","EMAIL":"EMAIL",
         "ADDRESS":"ADDRESS","BANK":"BANK","VEHICLE":"VEHICLE"}
PH = re.compile(r"\{([A-Z]+\d?)\}")

def fill(template, r, P, lang):
    values, items = {}, []
    latin_in_urdu = (lang == "ur" and r.random() < 0.2)   # mixed script on purpose
    def val(key):
        if key in values: return values[key]
        t = LABEL[key]
        v = {"NAME": lambda: mk_name(r, P, lang, latin_in_urdu), "CNIC": lambda: mk_cnic(r),
             "PHONE": lambda: mk_phone(r), "EMAIL": lambda: mk_email(r, P),
             "ADDRESS": lambda: mk_address(r, P, lang), "BANK": lambda: mk_bank(r),
             "VEHICLE": lambda: mk_vehicle(r)}[t]()
        if key == "NAME2":
            while v == values.get("NAME"): v = mk_name(r, P, lang, latin_in_urdu)
        values[key] = v
        return v
    out_text, out_red, last = [], [], 0
    for m in PH.finditer(template):
        out_text.append(template[last:m.start()]); out_red.append(template[last:m.start()])
        v = val(m.group(1)); t = LABEL[m.group(1)]
        out_text.append(v); out_red.append(f"[{t}]")
        if (t, v) not in items: items.append((t, v))
        last = m.end()
    out_text.append(template[last:]); out_red.append(template[last:])
    return "".join(out_text), "".join(out_red), items

def format_output(redacted, items):
    lines = [f"- {t}: {v}" for t, v in items] or ["- none"]
    return "REDACTED:\n" + redacted + "\nFOUND:\n" + "\n".join(lines)

def make_example(r, P, idx, split):
    lang = r.choices(["en", "ru", "ur"], weights=[40, 35, 25])[0]
    pool = {"en": (P.en, P.en_clean), "ru": (P.ru, P.ru_clean), "ur": (P.ur, P.ur_clean)}[lang]
    parts_text, parts_red, items = [], [], []
    n_sent = 1 if r.random() < 0.7 else r.choice([2, 3])
    clean_example = r.random() < 0.10
    used = set()
    for _ in range(n_sent):
        src = pool[1] if clean_example else (pool[0] if (r.random() < 0.9 or not parts_text) else pool[1])
        choices = [t for t in src if t not in used] or src
        tpl = r.choice(choices); used.add(tpl)
        t, red, it = fill(tpl, r, P, lang)
        parts_text.append(t); parts_red.append(red)
        for x in it:
            if x not in items: items.append(x)
    text, red = " ".join(parts_text), " ".join(parts_red)
    return {"id": f"{split}-{idx:05d}", "lang": lang, "input": text, "redacted": red,
            "items": [{"type": t, "text": v} for t, v in items],
            "output": format_output(red, items)}

def build(split_name, n, seed, P, forbidden=None):
    r = random.Random(seed); rows, seen = [], set(forbidden or [])
    tries = 0
    while len(rows) < n and tries < n * 50:
        tries += 1
        ex = make_example(r, P, len(rows), split_name)
        if ex["input"] in seen: continue
        seen.add(ex["input"]); rows.append(ex)
    return rows

def to_chat(row):
    return {"messages": [{"role": "system", "content": SYSTEM},
                         {"role": "user", "content": row["input"]},
                         {"role": "assistant", "content": row["output"]}],
            **{k: row[k] for k in ("id", "lang")}}

def write(path, rows, chat=False):
    with open(path, "w", encoding="utf-8") as f:
        for r in rows: f.write(json.dumps(to_chat(r) if chat else r, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="data"); ap.add_argument("--train", type=int, default=3200)
    ap.add_argument("--val", type=int, default=400); ap.add_argument("--test", type=int, default=400)
    ap.add_argument("--seed", type=int, default=2026)
    a = ap.parse_args()
    import os; os.makedirs(a.out, exist_ok=True)
    tr = build("train", a.train, a.seed, Pools("train"))
    va = build("val", a.val, a.seed + 1, Pools("train"), forbidden={x["input"] for x in tr})
    te = build("test", a.test, a.seed + 2, Pools("test"), forbidden={x["input"] for x in tr + va})
    write(f"{a.out}/train.jsonl", tr, chat=True); write(f"{a.out}/val.jsonl", va, chat=True)
    write(f"{a.out}/test_raw.jsonl", te)            # raw = has gold items, used by score.py
    write(f"{a.out}/train_raw.jsonl", tr)
    for name, rows in (("train", tr), ("val", va), ("test", te)):
        c = collections.Counter(x["lang"] for x in rows)
        t = collections.Counter(i["type"] for x in rows for i in x["items"])
        clean = sum(1 for x in rows if not x["items"])
        print(name, len(rows), dict(c), "clean:", clean, dict(t))
