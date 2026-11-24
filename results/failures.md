# Pehchan Guard - failure analysis (training run 1, 24 Nov 2026)

Scores: held-out test F1 0.970 - hard set F1 0.883 - base model F1 0.008 / 0.000.

## Held-out test: 43 of 400 examples have at least one error

### test-00008 (ur)
Input: جزاک اللہ، فارم جمع کرا دیا ہے۔ میرا نام ماہ نور رانا اور ای میل rimshaaziz98@office.pk ہے۔ ادائیگی اس اکاؤنٹ میں کر دیں: PK06 BKIP 2679 7604 1201 2785، اکاؤنٹ ہولڈر کا نام دعا ہے۔ بچے کا نام مہوش ہے، والد کا نمبر 0337 7158464 ہے، اسکول فارم کے لیے شناختی کارڈ 45068-5230078-3 درکار ہے۔
Missed/leaked: [('NAME', 'دعا')]

### test-00015 (ru)
Input: Mehman Pasha kal aa rahe hain, un ko 081-8616640 par airport ka rasta bata dein.
Missed/leaked: [('NAME', 'Pasha')]
Wrongly flagged: [('NAME', 'Mehman Pasha')]

### test-00020 (ur)
Input: میرا ای میل غلط لکھا گیا ہے، درست ای میل tayyaba.safdar@outlook.com ہے، نام Hammad۔ مریم صاحب کی تنخواہ PK51JSBL2562724011117942 میں آتی ہے، شناختی کارڈ 54477-9627537-8 نوٹ کر لیں۔ بینک 5 فروری کو چھٹی کی وجہ سے بند رہے گا۔
Missed/leaked: [('NAME', 'مریم'), ('NAME', 'Hammad')]
Wrongly flagged: [('NAME', 'Hammad۔ مریم')]

### test-00034 (ur)
Input: احسان عزیز کا موبائل +92 316 6874995 بند مل رہا ہے، ان کے بھائی طوبیٰ عثمانی کو بتا دیں۔ میرا ای میل غلط لکھا گیا ہے، درست ای میل rashid.dar@outlook.com ہے، نام ارسلان بیگ۔
Missed/leaked: [('EMAIL', 'rashid.dar@outlook.com')]
Wrongly flagged: [('NAME', 'rashid.dar@outlook.com')]

### test-00037 (ru)
Input: Cheque Ehsan Wattu ke naam banega, account 4870838656 aur CNIC 25663-2206990-5 confirm kar dein. Bhai mera CNIC gum ho gaya hai, naam Minahil Usmani hai, mil jaye to 0343 0010444 par call kar dein. Mehman Yusuf Baig kal aa rahe hain, un ko +92 301 6576452 par airport ka rasta bata dein.
Missed/leaked: [('NAME', 'Yusuf Baig')]
Wrongly flagged: [('NAME', 'Mehman Yusuf Baig')]

### test-00040 (ru)
Input: Shadi ka card makan 32, Lalazar, Gujranwala par bhejna hai, Babar Ghani ke naam se. Mehman Mehwish kal aa rahe hain, un ko 03217336680 par airport ka rasta bata dein.
Missed/leaked: [('PHONE', '03217336680'), ('NAME', 'Mehwish')]
Wrongly flagged: [('NAME', 'Mehman Mehwish'), ('NAME', 'Shadi'), ('BANK', '03217336680')]

### test-00050 (ru)
Input: Rimsha ka mobile +92-303-1244341 band mil raha hai, un ke bhai Rimsha Wattu ko bata dein. Raheel sahab ki salary PK09JSBL4798406726948423 mein aati hai, CNIC 25165-0446141-4 note kar lein. Mehman Maryam Sheikh kal aa rahe hain, un ko +92 342 2198511 par airport ka rasta bata dein.
Wrongly flagged: [('NAME', 'Mehman')]

### test-00065 (ur)
Input: جزاک اللہ، فارم جمع کرا دیا ہے۔ میرا نام ہما اور ای میل yusuf.shabbir@yahoo.com ہے۔ فارم میں والد کا نام جنید اور اپنا نام شیریں منظور لکھا ہے، شناختی کارڈ 16462-4432256-3۔ چیک Maryam Ghani کے نام بنے گا، اکاؤنٹ 51437988312709 اور شناختی کارڈ 71165-3492101-4 تصدیق کر دیں۔
Missed/leaked: [('CNIC', '71165-3492101-4'), ('BANK', '51437988312709')]

### test-00101 (ur)
Input: مہمان شیریں عزیز کل آ رہے ہیں، ان کو 0328-9675992 پر ایئرپورٹ کا راستہ بتا دیں۔ میٹنگ کل سہ پہر تین بجے مرکزی کانفرنس روم میں ہے۔
Missed/leaked: [('NAME', 'شیریں عزیز')]
Wrongly flagged: [('NAME', 'شیریں')]

### test-00106 (ru)
Input: Shadi ka card ghar 432 street 2 Allama Iqbal Colony Kamalia par bhejna hai, Salma Dar ke naam se.
Wrongly flagged: [('NAME', 'Shadi')]

### test-00109 (ru)
Input: Meeting kal 3 baje hai, Maryam sab ko +92-340-9379086 par yaad dila dein. Mehman Rashid kal aa rahe hain, un ko 0340-2753427 par airport ka rasta bata dein.
Missed/leaked: [('NAME', 'Rashid')]
Wrongly flagged: [('NAME', 'Mehman Rashid')]

### test-00127 (ur)
Input: میرا اکاؤنٹ نمبر 3746597859626 ہے، نام طوبیٰ لکھنا ہے۔
Missed/leaked: [('NAME', 'طوبیٰ')]
Wrongly flagged: [('NAME', 'طوبی')]

### test-00139 (ru)
Input: Dua Ansari ka mobile +92-326-0557053 band mil raha hai, un ke bhai Qasim Ghani ko bata dein.
Missed/leaked: [('NAME', 'Dua Ansari')]
Wrongly flagged: [('NAME', 'Ansari')]

### test-00141 (ru)
Input: Mehman Yasir Wattu kal aa rahe hain, un ko 03262631313 par airport ka rasta bata dein.
Missed/leaked: [('NAME', 'Yasir Wattu')]
Wrongly flagged: [('NAME', 'Mehman Yasir Wattu')]

### test-00144 (ru)
Input: Mehman Maryam kal aa rahe hain, un ko 0315-4553497 par airport ka rasta bata dein.
Missed/leaked: [('NAME', 'Maryam')]
Wrongly flagged: [('NAME', 'Mehman Maryam')]

### test-00178 (ur)
Input: میرا اکاؤنٹ نمبر PK16 ALFH 9889 4334 2205 7294 ہے، نام فرزانہ رانا لکھنا ہے۔ میٹنگ کل تین بجے ہے، یوسف سب کو 0334-8096822 پر یاد دلا دیں۔
Missed/leaked: [('PHONE', '0334-8096822')]

### test-00196 (ru)
Input: Form mein walid ka naam Hammad aur apna naam Fareeha Usmani likha hai, CNIC 7600625478754.
Missed/leaked: [('NAME', 'Fareeha Usmani')]
Wrongly flagged: [('NAME', 'Fareeha')]

### test-00218 (ru)
Input: Shadi ka card ghar number 239, gali 51, mohalla Bahadurabad, Jhelum par bhejna hai, Babar Shabbir ke naam se.
Wrongly flagged: [('NAME', 'Shadi')]

### test-00230 (ur)
Input: مہمان راشد کل آ رہے ہیں، ان کو 041-1539321 پر ایئرپورٹ کا راستہ بتا دیں۔
Missed/leaked: [('NAME', 'راشد')]
Wrongly flagged: [('NAME', 'راشد کل آ رہے ہیں')]

### test-00234 (ru)
Input: Bhai payment PK02HABB1415490134345559 par kar do, account title Rashid Zahoor hai. Jazakallah, form jama kar diya hai. Mera naam Junaid Rana aur email arslanbaig23@mail.com.pk hai.
Missed/leaked: [('BANK', 'PK02HABB1415490134345559')]
Wrongly flagged: [('BANK', 'PK02HABB141549013434345559')]

### test-00237 (ru)
Input: Shadi ka card H# 7, St 7, Muslim Town, Kamalia par bhejna hai, Asad ke naam se. Mehman Ehsan Usmani kal aa rahe hain, un ko 0333-8201500 par airport ka rasta bata dein.
Missed/leaked: [('NAME', 'Ehsan Usmani')]
Wrongly flagged: [('NAME', 'Shadi'), ('NAME', 'Mehman Ehsan Usmani')]

### test-00240 (ru)
Input: Shadi ka card ghar 240 street 50 University Town Mandi Bahauddin par bhejna hai, Tuba ke naam se.
Wrongly flagged: [('NAME', 'Shadi')]

### test-00257 (ru)
Input: Shadi ka card makan 34, Malir, Dera Ghazi Khan par bhejna hai, Farzana Baig ke naam se. Traffic police ne gaari MNA 6693 ka challan kar diya, malik Farzana Pasha ko 0334-3438147 par bata dein.
Wrongly flagged: [('NAME', 'Shadi')]

### test-00265 (ru)
Input: Shadi ka card Flat 96, Block A, Allama Iqbal Colony, Sahiwal par bhejna hai, Farzana Aziz ke naam se.
Wrongly flagged: [('NAME', 'Shadi')]

### test-00266 (ru)
Input: Shadi ka card House 227, Street 15, Allama Iqbal Colony, Vehari par bhejna hai, Hammad Pasha ke naam se.
Wrongly flagged: [('NAME', 'Shadi')]

### test-00268 (ru)
Input: Mehman Raheel Aziz kal aa rahe hain, un ko 03036272677 par airport ka rasta bata dein.
Missed/leaked: [('NAME', 'Raheel Aziz')]
Wrongly flagged: [('NAME', 'Mehman Raheel Aziz')]

### test-00283 (ru)
Input: Mehman Bilal Usmani kal aa rahe hain, un ko 0328-1729072 par airport ka rasta bata dein. Bachay ka naam Hammad hai, walid ka number 0322 9919039, school form ke liye CNIC 53553-6743017-5 chahiye. Cheque Wattu ke naam banega, account PK14SCBL5963079553232568 aur CNIC 39102-8294890-0 confirm kar dein.
Missed/leaked: [('NAME', 'Bilal Usmani'), ('NAME', 'Wattu')]
Wrongly flagged: [('NAME', 'Mehman Bilal Usmani')]

### test-00288 (ru)
Input: Mehman Yasir Safdar kal aa rahe hain, un ko 0332 8681327 par airport ka rasta bata dein. Mera account number 2201-5240383512 hai, naam Shireen Usmani likhna.
Missed/leaked: [('NAME', 'Yasir Safdar')]
Wrongly flagged: [('NAME', 'Mehman Yasir Safdar')]

### test-00291 (ru)
Input: Mehman Arslan Baig kal aa rahe hain, un ko 022-7189890 par airport ka rasta bata dein.
Missed/leaked: [('NAME', 'Arslan Baig')]
Wrongly flagged: [('NAME', 'Mehman Arslan Baig')]

### test-00300 (ru)
Input: Bhai payment PK54 HABB 8873 3137 3958 6183 par kar do, account title Dua hai.
Missed/leaked: [('NAME', 'Dua')]

### test-00302 (ru)
Input: Mehman Laiba Ansari kal aa rahe hain, un ko 051-97583609 par airport ka rasta bata dein. Form mein walid ka naam Sadia Wattu aur apna naam Minahil Ansari likha hai, CNIC 39246-7309761-0. Bank 5 February ko chuttion ki wajah se band rahega.
Missed/leaked: [('NAME', 'Laiba Ansari')]
Wrongly flagged: [('NAME', 'Mehman Laiba Ansari')]

### test-00307 (ru)
Input: Shadi ka card House No. 268, Malir, Sahiwal par bhejna hai, Bilal Usmani ke naam se.
Wrongly flagged: [('NAME', 'Shadi')]

### test-00316 (ur)
Input: مہمان دعا کل آ رہے ہیں، ان کو +92-315-5386759 پر ایئرپورٹ کا راستہ بتا دیں۔
Missed/leaked: [('NAME', 'دعا')]

### test-00324 (ru)
Input: Mehman Tayyaba Pasha kal aa rahe hain, un ko 03412792045 par airport ka rasta bata dein.
Missed/leaked: [('NAME', 'Tayyaba Pasha')]
Wrongly flagged: [('NAME', 'Mehman Tayyaba Pasha')]

### test-00337 (ur)
Input: ہما منظور کا موبائل 0304-7672888 بند مل رہا ہے، ان کے بھائی مناہل پاشا کو بتا دیں۔
Missed/leaked: [('NAME', 'ہما منظور')]

### test-00350 (ru)
Input: Shadi ka card makan 131, Allama Iqbal Colony, Gujranwala par bhejna hai, Ehsan ke naam se.
Wrongly flagged: [('NAME', 'Shadi')]

### test-00354 (ru)
Input: Mehman Salma Ghani kal aa rahe hain, un ko 0320-8167246 par airport ka rasta bata dein.
Missed/leaked: [('NAME', 'Salma Ghani')]
Wrongly flagged: [('NAME', 'Mehman Salma Ghani')]

### test-00361 (ru)
Input: Meeting kal 3 baje hai, Sadia Dar sab ko 03172150060 par yaad dila dein.
Missed/leaked: [('PHONE', '03172150060')]
Wrongly flagged: [('BANK', '03172150060')]

### test-00369 (ru)
Input: Dua Shabbir ka mobile 022-9518856 band mil raha hai, un ke bhai Mahnoor Wattu ko bata dein.
Missed/leaked: [('NAME', 'Dua Shabbir')]
Wrongly flagged: [('NAME', 'Shabbir')]

### test-00387 (ru)
Input: Mehman Nighat Pasha kal aa rahe hain, un ko +92 322 2255389 par airport ka rasta bata dein.
Missed/leaked: [('NAME', 'Nighat Pasha')]
Wrongly flagged: [('NAME', 'Mehman Nighat Pasha')]

### test-00390 (ru)
Input: Mehman Salma kal aa rahe hain, un ko 0300-8176038 par airport ka rasta bata dein. Meeting kal 3 baje hai, Asad sab ko 0321-5258008 par yaad dila dein. Form mein walid ka naam Yusuf Manzoor aur apna naam Nighat Aziz likha hai, CNIC 7764433770441.
Missed/leaked: [('NAME', 'Salma')]
Wrongly flagged: [('NAME', 'Mehman Salma')]

### test-00393 (ru)
Input: Shadi ka card makan 176, DHA Phase 2, Kamalia par bhejna hai, Aziz ke naam se.
Wrongly flagged: [('NAME', 'Shadi')]

### test-00397 (ur)
Input: میرا ای میل غلط لکھا گیا ہے، درست ای میل arslan_usmani62@yahoo.com ہے، نام جنید۔ سڑک کی مرمت اس ماہ کے آخر تک مکمل ہو جائے گی۔ یوسف گجر کا موبائل 0317-5141308 بند مل رہا ہے، ان کے بھائی دعا انصاری کو بتا دیں۔
Missed/leaked: [('NAME', 'یوسف گجر')]
Wrongly flagged: [('NAME', 'یوسف')]

## Hard set: 18 of 60 examples have at least one error

### hard-006
Input: KYC update required for account holder Col. (R) Tariq Aziz, IBAN PK91 MEZN 0001 2345 6789 0123, mobile 0300-9456123.
Missed/leaked: [('NAME', 'Tariq Aziz')]
Wrongly flagged: [('NAME', 'Col. (R) Tariq Aziz')]
Model output: REDACTED:
KYC update required for account holder [NAME], IBAN [BANK], mobile [PHONE].
FOUND:
- NAME: Col. (R) Tariq Aziz
- BANK: PK91 MEZN 0001 2345 6789 0123
- PHONE: 0300-9456123

### hard-010
Input: Kindly remit the consultancy fee to PK24 HABB 0012 3456 7890 1234, account title Dr. Sana Tariq, and share the receipt on sana.tariq@hospital.org.pk.
Missed/leaked: [('NAME', 'Sana Tariq')]
Wrongly flagged: [('NAME', 'Dr. Sana Tariq')]
Model output: REDACTED:
Kindly remit the consultancy fee to [BANK], account title [NAME], and share the receipt on [EMAIL].
FOUND:
- BANK: PK24 HABB 0012 3456 7890 1234
- NAME: Dr. Sana Tariq
- EMAIL: sana.tariq@hospital.org.pk

### hard-023
Input: shop ka address: Dukaan 5, Urdu Bazaar, Lahore, malik Abdul Hafeez, 0321-4433221
Missed/leaked: [('NAME', 'Abdul Hafeez')]
Wrongly flagged: [('NAME', 'malik Abdul Hafeez')]
Model output: REDACTED:
shop ka address: [ADDRESS], [NAME], [PHONE]
FOUND:
- ADDRESS: Dukaan 5, Urdu Bazaar, Lahore
- NAME: malik Abdul Hafeez
- PHONE: 0321-4433221

### hard-028
Input: مریض خالدہ پروین کو داخل کر لیا گیا ہے، اہل خانہ 0321-6655443 پر رابطہ کریں۔
Missed/leaked: [('NAME', 'خالدہ پروین')]
Wrongly flagged: [('NAME', 'مریض خالدہ پروین')]
Model output: REDACTED:
[NAME] کو داخل کر لیا گیا ہے، اہل خانہ [PHONE] پر رابطہ کریں۔
FOUND:
- NAME: مریض خالدہ پروین
- PHONE: 0321-6655443

### hard-029
Input: براہ کرم رقم اس اکاؤنٹ میں بھیجیں: PK77 MEZN 0102 0304 0506 0708، اکاؤنٹ ہولڈر حاجی محمد اسلم ہیں۔
Missed/leaked: [('NAME', 'محمد اسلم')]
Wrongly flagged: [('NAME', 'حاجی محمد اسلم')]
Model output: REDACTED:
براہ کرم رقم اس اکاؤنٹ میں بھیجیں: [BANK]، اکاؤنٹ ہولڈر [NAME] ہیں۔
FOUND:
- BANK: PK77 MEZN 0102 0304 0506 0708
- NAME: حاجی محمد اسلم

### hard-032
Input: اس گاڑی LEA-19-3322 کے مالک میاں محمد نواز ہیں، ان کا نمبر 0322-9988776 ہے۔
Missed/leaked: [('NAME', 'محمد نواز')]
Wrongly flagged: [('NAME', 'میاں محمد نواز')]
Model output: REDACTED:
اس گاڑی [VEHICLE] کے مالک [NAME] ہیں، ان کا نمبر [PHONE] ہے۔
FOUND:
- VEHICLE: LEA-19-3322
- NAME: میاں محمد نواز
- PHONE: 0322-9988776

### hard-034
Input: شکایت کنندہ نسرین بی بی، پتہ محلہ رسول نگر، نزد جامع مسجد، گجرات، رابطہ نمبر 0333-7766554۔
Missed/leaked: [('ADDRESS', 'محلہ رسول نگر، نزد جامع مسجد، گجرات')]
Wrongly flagged: [('ADDRESS', 'محلہ رسول نگر، نزد جامع مسجد')]
Model output: REDACTED:
شکایت کنندہ [NAME]، پتہ [ADDRESS]، رابطہ نمبر [PHONE]۔
FOUND:
- NAME: نسرین بی بی
- ADDRESS: محلہ رسول نگر، نزد جامع مسجد
- PHONE: 0333-7766554

### hard-035
Input: تمام اہل محلہ کو اطلاع دی جاتی ہے کہ چوہدری محمد صدیق کے بیٹے کی شادی ہے، رابطہ 0345-5544332۔
Missed/leaked: [('NAME', 'محمد صدیق')]
Wrongly flagged: [('NAME', 'چوہدری محمد صدیق')]
Model output: REDACTED:
تمام اہل محلہ کو اطلاع دی جاتی ہے کہ [NAME] کے بیٹے کی شادی ہے، رابطہ [PHONE]۔
FOUND:
- NAME: چوہدری محمد صدیق
- PHONE: 0345-5544332

### hard-038
Input: گزشتہ روز محمد الیاس ولد محمد صادق ساکن چک نمبر 12، تحصیل چونیاں، ضلع قصور نے تھانے میں رپورٹ درج کرائی کہ ان کی گاڑی LEB-4410 چوری ہو گئی ہے۔ رابطہ نمبر 0301-6677885 اور شناختی کارڈ 35102-9988776-3 رپورٹ میں درج ہے۔
Missed/leaked: [('ADDRESS', 'چک نمبر 12، تحصیل چونیاں، ضلع قصور')]
Wrongly flagged: [('ADDRESS', 'چک نمبر 12'), ('ADDRESS', 'قصور'), ('ADDRESS', 'چونیاں')]
Model output: REDACTED:
گزشتہ روز [NAME] ولد [NAME] ساکن چک نمبر [ADDRESS]، تحصیل [ADDRESS]، ضلع [ADDRESS] نے تھانے میں رپورٹ درج کرائی کہ ان کی گاڑی [VEHICLE] چوری ہو گئی ہے۔ رابطہ نمبر [PHONE] اور شناختی کارڈ [CNIC] رپورٹ میں درج ہے۔
FOUND:
- NAME: محمد الیاس
- NAME: محمد صادق
- ADDRESS: چک نمبر 12
- ADDRESS: چ

### hard-040
Input: علی رضا will bring the documents kal subah, his CNIC is 35202-7788990-1 aur address House 9, Street 14, F-7/2, Islamabad hai.
Wrongly flagged: [('NAME', 'kal subah')]
Model output: REDACTED:
[NAME] will bring the documents [NAME], his CNIC is [CNIC] and address [ADDRESS].
FOUND:
- NAME: علی رضا
- NAME: kal subah
- CNIC: 35202-7788990-1
- ADDRESS: House 9, Street 14, F-7/2, Islamabad

### hard-041
Input: Assalam o Alaikum, this is Dr. Ayesha Rahman from City Hospital, mareez ki reports ayesha.rahman@cityhospital.pk par bhej dein.
Missed/leaked: [('NAME', 'Ayesha Rahman')]
Wrongly flagged: [('NAME', 'Dr. Ayesha Rahman'), ('ADDRESS', 'City Hospital'), ('NAME', 'mareez')]
Model output: REDACTED:
Assalam o Alaikum, this is [NAME] from [ADDRESS], [NAME] ki reports [EMAIL] par bhej dein.
FOUND:
- NAME: Dr. Ayesha Rahman
- ADDRESS: City Hospital
- NAME: mareez
- EMAIL: ayesha.rahman@cityhospital.pk

### hard-044
Input: Kal meeting mein Sarah Khan aur علی حسن dono honge, Sarah ka email sarah.khan@techfirm.com hai.
Wrongly flagged: [('NAME', 'Sarah')]
Model output: REDACTED:
Kal meeting mein [NAME] aur [NAME] dono honge, [NAME] ka email [EMAIL] hai.
FOUND:
- NAME: Sarah Khan
- NAME: علی حسن
- NAME: Sarah
- EMAIL: sarah.khan@techfirm.com

### hard-047
Input: email id: ali.raza @ gmail.com par bhejna, aur cc hr @ office.pk ko bhi kar dena
Missed/leaked: [('EMAIL', 'hr @ office.pk'), ('EMAIL', 'ali.raza @ gmail.com')]
Wrongly flagged: [('EMAIL', 'ali.raza@gmail.com'), ('EMAIL', 'hr@office.pk')]
Model output: REDACTED:
email id: [EMAIL] par bhejna, aur cc [EMAIL] ko bhi kar dena
FOUND:
- EMAIL: ali.raza@gmail.com
- EMAIL: hr@office.pk

### hard-050
Input: Account no. 1020 3040 5060 7080 title S. M. Rizwan bank meezan, urgent transfer kar dein
Wrongly flagged: [('ADDRESS', 'meezan, urgent')]
Model output: REDACTED:
Account no. [BANK] title [NAME] bank [ADDRESS] urgent transfer kar dein
FOUND:
- BANK: 1020 3040 5060 7080
- NAME: S. M. Rizwan
- ADDRESS: meezan, urgent

### hard-051
Input: gari num le a 4410 chori ho gayi hai malik Rana Sanaullah
Missed/leaked: [('VEHICLE', 'le a 4410')]
Wrongly flagged: [('ADDRESS', '4410')]
Model output: REDACTED:
gari num le a [ADDRESS] chori ho gayi hai malik [NAME]
FOUND:
- ADDRESS: 4410
- NAME: Rana Sanaullah

### hard-054
Input: Kamran Shahid aur David Mathew ki meeting kal hai, David ka number +92 321 4455667 hai.
Wrongly flagged: [('NAME', 'David')]
Model output: REDACTED:
[NAME] aur [NAME] ki meeting kal hai, [NAME] ka number [PHONE] hai.
FOUND:
- NAME: Kamran Shahid
- NAME: David Mathew
- NAME: David
- PHONE: +92 321 4455667

### hard-057
Input: Kal barish ka imkan hai, darja hararat 12 degree tak reh sakta hai.
Wrongly flagged: [('NAME', 'hararat')]
Model output: REDACTED:
Kal barish ka imkan hai, darja [NAME] 12 degree tak reh sakta hai.
FOUND:
- NAME: hararat

### hard-062
Input: aslam bhai ko paise bhej diye hain PK12 MEZN 0009 8765 4321 0987 mein, Muhammad Aslam ko call kar ke bata dein 0301-3344556
Wrongly flagged: [('NAME', 'aslam')]
Model output: REDACTED:
[NAME] bhai ko paise bhej diye hain [BANK] mein, [NAME] ko call kar ke bata dein [PHONE].
FOUND:
- NAME: aslam
- BANK: PK12 MEZN 0009 8765 4321 0987
- NAME: Muhammad Aslam
- PHONE: 0301-3344556