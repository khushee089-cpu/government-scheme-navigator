"""Hindi display copy for scheme data; original source records remain unchanged."""

from copy import deepcopy
import re


# department, category, short description, key benefits
SCHEME_TEXT_HI = {
    "SCHEME-001": ("कृषि एवं किसान कल्याण विभाग, कृषि एवं किसान कल्याण मंत्रालय", "कृषि", "पात्र भूमिधारक किसान परिवारों को सीधे उनके बैंक खातों में प्रति वर्ष ₹6,000 की आय सहायता तीन समान चार-मासिक किस्तों में दी जाती है।", "प्रत्यक्ष लाभ अंतरण (DBT) के माध्यम से ₹2,000 की तीन किस्तों में प्रति वर्ष ₹6,000 सीधे बैंक खाते में जमा किए जाते हैं।"),
    "SCHEME-002": ("राष्ट्रीय स्वास्थ्य प्राधिकरण (NHA), स्वास्थ्य एवं परिवार कल्याण मंत्रालय", "स्वास्थ्य सेवा", "सरकार द्वारा वित्तपोषित स्वास्थ्य सुरक्षा योजना, जिसमें सूचीबद्ध सरकारी और निजी अस्पतालों में द्वितीयक एवं तृतीयक उपचार के लिए प्रति परिवार प्रति वर्ष ₹5 लाख तक का स्वास्थ्य कवर मिलता है।", "अस्पताल में भर्ती के लिए प्रति परिवार प्रति वर्ष ₹5,00,000 तक कैशलेस कवर। इसमें पहले से मौजूद बीमारियां, जांच, सर्जरी, दवाएं और गहन चिकित्सा शामिल हैं।"),
    "SCHEME-003": ("ग्रामीण विकास मंत्रालय", "आवास", "ग्रामीण बेघर परिवारों और कच्चे घरों में रहने वाले परिवारों को शौचालय, एलपीजी और बिजली जैसी बुनियादी सुविधाओं सहित पक्का घर बनाने के लिए वित्तीय सहायता।", "मैदानी क्षेत्रों में ₹1,20,000 और पहाड़ी, कठिन तथा पूर्वोत्तर क्षेत्रों में ₹1,30,000 की सहायता। इसके अतिरिक्त MGNREGS के तहत 90–95 दिन का अकुशल श्रम और SBM के तहत शौचालय के लिए ₹12,000 की सहायता।"),
    "SCHEME-004": ("आवास एवं शहरी कार्य मंत्रालय", "आवास", "पात्र शहरी परिवारों को पक्का घर बनाने, खरीदने या सुधारने के लिए ब्याज सब्सिडी अथवा सीधे वित्तीय सहायता के रूप में आवास सहायता।", "₹2,50,000 तक की प्रत्यक्ष वित्तीय सहायता या 12 वर्षों के लिए ₹25 लाख तक के गृह ऋण पर 4% तक ब्याज सब्सिडी।"),
    "SCHEME-005": ("पेट्रोलियम एवं प्राकृतिक गैस मंत्रालय", "सामाजिक कल्याण एवं ऊर्जा", "वंचित परिवारों की वयस्क महिलाओं को बिना जमा राशि के एलपीजी कनेक्शन, पहली रिफिल और चूल्हा उपलब्ध कराया जाता है।", "बिना जमा राशि का एलपीजी कनेक्शन, 14.2 किग्रा या 5 किग्रा सिलेंडर की पहली रिफिल, दो बर्नर वाला चूल्हा और पात्रता के अनुसार सिलेंडर सब्सिडी।"),
    "SCHEME-006": ("वित्तीय सेवा विभाग, वित्त मंत्रालय", "सूक्ष्म व्यवसाय एवं उद्यम", "आय पैदा करने वाले सूक्ष्म उद्यमों के लिए बैंकों, NBFC और MFI के माध्यम से ₹10 लाख तक और पात्र पुराने तरुण उधारकर्ताओं के लिए ₹20 लाख तक बिना जमानत संस्थागत ऋण।", "बिना जमानत तीन ऋण श्रेणियां: शिशु (₹50,000 तक), किशोर (₹50,000 से ₹5,00,000) और तरुण (₹5,00,000 से ₹10,00,000; तरुण प्लस में ₹20 लाख तक)।"),
    "SCHEME-007": ("सूक्ष्म, लघु एवं मध्यम उद्यम मंत्रालय", "कारीगर एवं MSME", "पारंपरिक कारीगरों को विश्वकर्मा प्रमाणपत्र और पहचान पत्र, कौशल प्रशिक्षण व दैनिक भत्ता, ₹15,000 का औजार प्रोत्साहन तथा कम ब्याज पर बिना जमानत उद्यम ऋण दिया जाता है।", "प्रशिक्षण के दौरान ₹500 प्रतिदिन भत्ता, ₹15,000 का औजार अनुदान, पहली और दूसरी किस्त में क्रमशः ₹1 लाख और ₹2 लाख तक का बिना जमानत ऋण तथा 5% रियायती ब्याज दर।"),
    "SCHEME-008": ("आवास एवं शहरी कार्य मंत्रालय", "आजीविका एवं MSME", "स्ट्रीट वेंडरों को अपना काम फिर से शुरू करने और बढ़ाने के लिए किफायती, बिना जमानत कार्यशील पूंजी ऋण।", "बिना जमानत ऋण: पहला ₹10,000 तक, समय पर भुगतान पर दूसरा ₹20,000 तक और तीसरा ₹50,000 तक। 7% ब्याज सब्सिडी तथा डिजिटल लेनदेन पर ₹1,200 प्रति वर्ष तक कैशबैक।"),
    "SCHEME-009": ("ग्रामीण विकास मंत्रालय", "सामाजिक सहायता एवं वरिष्ठ नागरिक", "गरीबी रेखा से नीचे रहने वाले वरिष्ठ नागरिकों को बुढ़ापे में बुनियादी सामाजिक सुरक्षा देने के लिए बिना अंशदान मासिक पेंशन।", "केंद्र से 60–79 वर्ष की आयु में ₹200 और 80 वर्ष या उससे अधिक आयु में ₹500 मासिक पेंशन। राज्य सरकारों की अतिरिक्त सहायता राज्य के अनुसार बदलती है।"),
    "SCHEME-010": ("सामाजिक न्याय एवं अधिकारिता मंत्रालय / जनजातीय कार्य मंत्रालय", "शिक्षा एवं छात्रवृत्ति", "कक्षा 11, 12, स्नातक, स्नातकोत्तर या व्यावसायिक पाठ्यक्रम में पढ़ रहे SC/ST विद्यार्थियों की अनिवार्य गैर-वापसी योग्य फीस और मासिक भत्ते के लिए छात्रवृत्ति।", "गैर-वापसी योग्य ट्यूशन और परीक्षा शुल्क की 100% प्रतिपूर्ति तथा मासिक भत्ता: छात्रावास में रहने वालों के लिए ₹13,500 प्रति वर्ष तक और अन्य विद्यार्थियों के लिए ₹7,000 प्रति वर्ष तक।"),
    "SCHEME-011": ("वित्तीय सेवा विभाग / SIDBI", "महिला एवं MSME", "नई (ग्रीनफील्ड) उद्यम स्थापना के लिए प्रत्येक बैंक शाखा से कम-से-कम एक SC/ST उधारकर्ता और एक महिला उधारकर्ता को ₹10 लाख से ₹1 करोड़ तक का बैंक ऋण।", "विनिर्माण, सेवा, कृषि-संबद्ध या व्यापार क्षेत्र में परियोजना लागत के 85% तक बैंक ऋण, रियायती ब्याज दर और ऋण गारंटी सुविधा।"),
    "SCHEME-012": ("पेंशन निधि विनियामक एवं विकास प्राधिकरण (PFRDA), वित्त मंत्रालय", "सामाजिक सुरक्षा एवं पेंशन", "असंगठित क्षेत्र के श्रमिकों को सेवानिवृत्ति में सुनिश्चित मासिक आय देने के लिए सरकार समर्थित स्वैच्छिक पेंशन योजना।", "अंशदान के अनुसार 60 वर्ष की आयु से ₹1,000, ₹2,000, ₹3,000, ₹4,000 या ₹5,000 की सुनिश्चित न्यूनतम मासिक पेंशन। सदस्य की मृत्यु पर पेंशन जीवनसाथी को और बाद में संचित राशि नामांकित व्यक्ति को मिलती है।"),
    "SCHEME-013": ("वित्तीय सेवा विभाग, वित्त मंत्रालय", "बीमा एवं सामाजिक सुरक्षा", "दुर्घटना में मृत्यु और स्थायी दिव्यांगता के विरुद्ध सुरक्षा देने वाला कम प्रीमियम का वार्षिक सरकारी व्यक्तिगत दुर्घटना बीमा।", "दुर्घटना में मृत्यु या स्थायी पूर्ण दिव्यांगता पर ₹2 लाख और स्थायी आंशिक दिव्यांगता पर ₹1 लाख का कवर। वार्षिक प्रीमियम ₹20 है और बैंक खाते से स्वतः कटता है।"),
    "SCHEME-014": ("डाक विभाग / वित्त मंत्रालय", "महिला एवं बाल कल्याण", "बालिकाओं की उच्च शिक्षा और विवाह के भविष्य के खर्च के लिए बनाई गई उच्च ब्याज वाली सरकारी लघु बचत योजना।", "सरकार द्वारा निर्धारित ब्याज दर, धारा 80C के तहत कर छूट तथा कर-मुक्त ब्याज और परिपक्वता राशि। खाता 21 वर्ष पूरे होने पर या 18 वर्ष की आयु के बाद विवाह पर परिपक्व होता है।"),
    "SCHEME-015": ("कौशल विकास एवं उद्यमिता मंत्रालय (MSDE) / NSDC", "कौशल विकास", "निःशुल्क अल्पकालिक उद्योग-आधारित प्रशिक्षण, सॉफ्ट स्किल, डिजिटल साक्षरता और रोजगार सहायता देने वाली प्रमुख कौशल प्रमाणन योजना।", "NSQF के अनुरूप निःशुल्क कौशल पाठ्यक्रम, सरकारी मान्यता प्राप्त प्रमाणपत्र, मूल्यांकन प्रोत्साहन, डिजिटल साक्षरता और रोजगार मेलों के माध्यम से नौकरी पाने में सहायता।"),
    "SCHEME-016": ("मत्स्य पालन, पशुपालन एवं डेयरी मंत्रालय, मत्स्य पालन विभाग", "मत्स्य पालन एवं कृषि", "मत्स्य पालन क्षेत्र के सतत विकास के लिए तालाब, बायोफ्लॉक इकाई, आधुनिक मछली पकड़ने के जहाज और शीत भंडारण श्रृंखला पर सहायता।", "हैचरी, जलीय कृषि इकाइयों और शीत श्रृंखला पर परियोजना लागत का 40% अनुदान सामान्य वर्ग के लिए और महिलाओं, SC तथा ST लाभार्थियों के लिए 60% तक।"),
    "SCHEME-017": ("कौशल विकास एवं उद्यमिता मंत्रालय (MSDE)", "कौशल एवं रोजगार", "प्रशिक्षण के दौरान युवाओं को सरकारी वजीफा सहायता देकर औद्योगिक प्रतिष्ठानों में अप्रेंटिसशिप प्रशिक्षण को बढ़ावा देने वाली योजना।", "सरकार निर्धारित मासिक वजीफे का 25%, अधिकतम ₹1,500 प्रति माह, DBT के माध्यम से प्रशिक्षु को देती है। साथ में व्यावहारिक प्रशिक्षण और राष्ट्रीय अप्रेंटिसशिप प्रमाणपत्र मिलता है।"),
    "SCHEME-018": ("महिला एवं बाल विकास विभाग, उत्तर प्रदेश सरकार", "महिला एवं बाल कल्याण", "उत्तर प्रदेश की राज्य योजना, जो बालिका के जन्म से स्नातक तक छह चरणों में वित्तीय सहायता देकर शिक्षा को बढ़ावा देती है।", "छह चरणों में कुल ₹25,000: जन्म पर ₹5,000, एक वर्ष के टीकाकरण पर ₹2,000, कक्षा 1 में प्रवेश पर ₹3,000, कक्षा 6 में ₹3,000, कक्षा 9 में ₹5,000 और डिग्री/डिप्लोमा में प्रवेश पर ₹7,000।"),
    "SCHEME-019": ("विशेष कार्यक्रम कार्यान्वयन विभाग, तमिलनाडु सरकार", "महिला कल्याण एवं सामाजिक सुरक्षा", "तमिलनाडु की योजना, जो गृहिणियों के अवैतनिक श्रम को मान्यता देते हुए पात्र परिवार की महिला मुखिया को बिना शर्त मासिक सहायता देती है।", "परिवार की महिला मुखिया के बैंक खाते में सीधे ₹1,000 प्रति माह, यानी ₹12,000 प्रति वर्ष जमा किए जाते हैं।"),
    "SCHEME-020": ("कौशल, रोजगार एवं उद्यमिता विभाग, राजस्थान सरकार", "युवा एवं रोजगार", "राजस्थान के शिक्षित बेरोजगार स्नातक युवाओं के लिए मासिक भत्ता और कौशल विकास योजना, जिसमें प्रतिदिन चार घंटे की इंटर्नशिप शामिल है।", "पुरुष स्नातक उम्मीदवारों को ₹4,000 प्रति माह और महिला, ट्रांसजेंडर तथा दिव्यांग उम्मीदवारों को ₹4,500 प्रति माह, अधिकतम दो वर्ष या रोजगार मिलने तक।"),
}


DOCUMENT_PHRASES_HI = {
    "Aadhaar Card": "आधार कार्ड", "Land Ownership Documents": "भूमि स्वामित्व दस्तावेज़",
    "Bank Account Passbook": "बैंक पासबुक", "Active Mobile Number": "सक्रिय मोबाइल नंबर",
    "Ration Card": "राशन कार्ड", "Income Certificate": "आय प्रमाणपत्र",
    "Residence Certificate": "निवास प्रमाणपत्र", "Residence Proof": "निवास प्रमाण",
    "Address Proof": "पता प्रमाण", "Identity Proof": "पहचान प्रमाण",
    "Caste Certificate": "जाति प्रमाणपत्र", "Birth Certificate": "जन्म प्रमाणपत्र",
    "Passport size photographs": "पासपोर्ट आकार के फोटो", "Passport size photograph": "पासपोर्ट आकार का फोटो",
    "Educational qualification certificates": "शैक्षणिक योग्यता प्रमाणपत्र", "Educational qualification certificate": "शैक्षणिक योग्यता प्रमाणपत्र",
    "Previous Year Marksheets": "पिछले वर्ष की अंकसूची", "Current Academic Year Fee Receipt": "वर्तमान शैक्षणिक वर्ष की फीस रसीद",
    "Student ID Card": "विद्यार्थी पहचान पत्र", "Bank Account details": "बैंक खाते का विवरण",
    "Active Savings Bank Account": "सक्रिय बचत बैंक खाता", "Active Mobile Phone Number": "सक्रिय मोबाइल नंबर",
    "Nominee Details": "नामांकित व्यक्ति का विवरण", "Proof of Business Enterprise": "व्यावसायिक उद्यम का प्रमाण",
    "Bank statement of last 6 months": "पिछले 6 महीनों का बैंक विवरण", "Certificate of Vending": "वेंडिंग प्रमाणपत्र",
    "Letter of Recommendation": "सिफारिश पत्र", "Driving License": "ड्राइविंग लाइसेंस", "Voter ID": "मतदाता पहचान पत्र",
    "PAN Card": "पैन कार्ड", "Passport": "पासपोर्ट", "Detailed Project Report": "विस्तृत परियोजना रिपोर्ट",
    "Lease agreement": "किरायानामा", "Lease deed": "पट्टा विलेख", "Udyam Certificate": "उद्यम प्रमाणपत्र",
    "Jan Aadhaar Card": "जन आधार कार्ड", "Mool Niwas Praman Patra": "मूल निवास प्रमाणपत्र",
    "Khatauni": "खतौनी", "Khasra": "खसरा", "Land Record": "भूमि अभिलेख", "Utility bill": "उपयोगिता बिल",
    "Electricity consumer number bill receipt": "बिजली उपभोक्ता संख्या वाली बिल रसीद", "Salary slips": "वेतन पर्चियां",
    "Affidavit": "शपथपत्र", "Smart Ration Card": "स्मार्ट राशन कार्ड", "BPL Ration Card": "बीपीएल राशन कार्ड",
    "BPL Certificate": "बीपीएल प्रमाणपत्र", "SECC Verification Proof": "SECC सत्यापन प्रमाण",
    "Family ID document": "परिवार पहचान दस्तावेज़", "Consent letter": "सहमति-पत्र",
    "Skill / Trade declaration": "कौशल/व्यवसाय की घोषणा", "KYC": "KYC", "Tehsildar": "तहसीलदार",
    "Graduation Degree Certificate": "स्नातक डिग्री प्रमाणपत्र", "Final Marksheet": "अंतिम अंकसूची",
    "linked with Aadhaar for OTP e-KYC": "OTP ई-KYC के लिए आधार से जुड़ा हुआ",
    "Land Record RoR": "भूमि अभिलेख RoR", "Job Card Number": "जॉब कार्ड संख्या",
    "current kutcha house or land site": "वर्तमान कच्चे घर या भूमि स्थल",
    "Family composition certificate": "परिवार के सदस्यों का प्रमाणपत्र",
    "Self-declaration": "स्व-घोषणा", "not possessing an LPG connection": "कि एलपीजी कनेक्शन नहीं है",
    "adult female applicant": "वयस्क महिला आवेदक", "Registration certificate": "पंजीकरण प्रमाणपत्र",
    "Shop & Establishment license": "दुकान एवं प्रतिष्ठान लाइसेंस", "Rent agreement": "किरायानामा",
    "machinery or items to be purchased with loan": "ऋण से खरीदी जाने वाली मशीनों या वस्तुओं",
    "Post Office Savings Account": "डाकघर बचत खाता", "auto-debit consent form": "ऑटो-डेबिट सहमति-पत्र",
    "Nominee identification": "नामांकित व्यक्ति की पहचान", "of the girl child": "बालिका का",
    "parent/legal guardian": "माता-पिता/कानूनी अभिभावक", "child and guardian": "बालिका और अभिभावक",
    "cash-flow projection": "नकदी प्रवाह का अनुमान", "business premises": "व्यावसायिक परिसर",
    "Net worth proof": "कुल संपत्ति का प्रमाण", "water body": "जलाशय", "DBT linked": "DBT से जुड़ा हुआ",
    "Uttar Pradesh Domicile": "उत्तर प्रदेश मूल निवास प्रमाणपत्र", "Admission proof": "प्रवेश का प्रमाण",
    "School Certificate": "विद्यालय प्रमाणपत्र", "relevant stage": "संबंधित चरण", "mother/guardian": "माता/अभिभावक",
    "Tamil Nadu": "तमिलनाडु", "Family Card": "परिवार कार्ड", "female head of family": "परिवार की महिला मुखिया",
    "Rajasthan Bonafide Domicile Certificate": "राजस्थान का मूल निवास प्रमाणपत्र",
    "Jan Aadhaar seeded": "जन आधार से जुड़ी हुई",
}

# Full-label translations take precedence over phrase substitutions so document
# names remain natural Hindi instead of becoming a word-by-word mix.
DOCUMENT_EXACT_HI = {
    "Aadhaar Card (linked with bank account)": "आधार कार्ड (बैंक खाते से जुड़ा हुआ)",
    "Land Ownership Documents (Khatauni / Khasra / Land Record RoR)": "भूमि स्वामित्व दस्तावेज़ (खतौनी / खसरा / भूमि अभिलेख RoR)",
    "Bank Account Passbook (DBT-enabled NPCI mapped)": "बैंक पासबुक (DBT सक्षम और NPCI से मैप की हुई)",
    "Active Mobile Number (linked with Aadhaar for OTP e-KYC)": "सक्रिय मोबाइल नंबर (OTP ई-KYC के लिए आधार से जुड़ा हुआ)",
    "Aadhaar Card of all family members": "परिवार के सभी सदस्यों के आधार कार्ड",
    "Ration Card / Family ID document": "राशन कार्ड / परिवार पहचान दस्तावेज़",
    "Income Certificate or SECC Verification Proof (if applicable)": "आय प्रमाणपत्र या SECC सत्यापन प्रमाण (यदि लागू हो)",
    "Aadhaar Card": "आधार कार्ड",
    "Bank Account Passbook (with IFSC and DBT linkage)": "बैंक पासबुक (IFSC और DBT लिंक सहित)",
    "MGNREGA Job Card Number (if available)": "MGNREGA जॉब कार्ड संख्या (यदि उपलब्ध हो)",
    "Consent letter to use Aadhaar data": "आधार डेटा के उपयोग के लिए सहमति-पत्र",
    "Photograph of current kutcha house or land site": "वर्तमान कच्चे घर या भूमि स्थल का फोटो",
    "Salary slips / Income Certificate / ITR": "वेतन पर्चियां / आय प्रमाणपत्र / ITR",
    "Urban Residence Proof (Utility bill, voter card, or lease agreement)": "शहरी निवास प्रमाण (उपयोगिता बिल, मतदाता पहचान पत्र या किरायानामा)",
    "Bank Account details": "बैंक खाते का विवरण",
    "Affidavit of not owning a pucca house": "पक्का मकान न होने का शपथपत्र",
    "Aadhaar Card of adult female applicant": "वयस्क महिला आवेदक का आधार कार्ड",
    "Ration Card or Family composition certificate": "राशन कार्ड या परिवार के सदस्यों का प्रमाणपत्र",
    "Bank Account Passbook (linked with Aadhaar)": "बैंक पासबुक (आधार से जुड़ी हुई)",
    "Proof of address (Aadhaar / Voter ID / Ration Card)": "पते का प्रमाण (आधार / मतदाता पहचान पत्र / राशन कार्ड)",
    "Self-declaration of not possessing an LPG connection": "एलपीजी कनेक्शन न होने की स्व-घोषणा",
    "Identity Proof (Aadhaar / Voter ID / PAN Card / Passport)": "पहचान प्रमाण (आधार / मतदाता पहचान पत्र / पैन कार्ड / पासपोर्ट)",
    "Address Proof (Utility bill / Rent agreement / Aadhaar)": "पता प्रमाण (उपयोगिता बिल / किरायानामा / आधार)",
    "Proof of Business Enterprise (Registration certificate / Shop & Establishment license / Udyam Certificate, if existing)": "व्यावसायिक उद्यम का प्रमाण (पंजीकरण प्रमाणपत्र / दुकान एवं प्रतिष्ठान लाइसेंस / उद्यम प्रमाणपत्र, यदि उपलब्ध हो)",
    "Bank statement of last 6 months": "पिछले 6 महीनों का बैंक विवरण",
    "Quotations of machinery or items to be purchased with loan": "ऋण से खरीदी जाने वाली मशीनों या वस्तुओं के मूल्य-प्रस्ताव",
    "Bank Account details (with IFSC and Aadhaar linkage)": "बैंक खाते का विवरण (IFSC और आधार लिंक सहित)",
    "Active Mobile number linked with Aadhaar": "आधार से जुड़ा सक्रिय मोबाइल नंबर",
    "Ration Card / Proof of family composition": "राशन कार्ड / परिवार के सदस्यों का प्रमाण",
    "Voter ID / Driving License": "मतदाता पहचान पत्र / ड्राइविंग लाइसेंस",
    "Certificate of Vending / ID Card issued by Urban Local Body or Letter of Recommendation (LoR)": "वेंडिंग प्रमाणपत्र / शहरी स्थानीय निकाय द्वारा जारी पहचान पत्र या सिफारिश पत्र (LoR)",
    "Aadhaar Card or Age verification proof": "आधार कार्ड या आयु सत्यापन प्रमाण",
    "BPL Ration Card / BPL Certificate": "बीपीएल राशन कार्ड / बीपीएल प्रमाणपत्र",
    "Bank Account Passbook (Aadhaar mapped)": "बैंक पासबुक (आधार से मैप की हुई)",
    "Passport size photographs": "पासपोर्ट आकार के फोटो",
    "Residence Certificate": "निवास प्रमाणपत्र",
    "Caste Certificate issued by competent revenue authority": "सक्षम राजस्व प्राधिकारी द्वारा जारी जाति प्रमाणपत्र",
    "Income Certificate of parents/guardian": "माता-पिता/अभिभावक का आय प्रमाणपत्र",
    "Previous Year Marksheets / Passing Certificate": "पिछले वर्ष की अंकसूची / उत्तीर्ण प्रमाणपत्र",
    "Current Academic Year Fee Receipt & Student ID Card": "वर्तमान शैक्षणिक वर्ष की फीस रसीद और विद्यार्थी पहचान पत्र",
    "Bank Account Passbook in student's own name": "विद्यार्थी के अपने नाम की बैंक पासबुक",
    "Caste Certificate (if applying under SC/ST quota)": "जाति प्रमाणपत्र (SC/ST आरक्षण के अंतर्गत आवेदन करने पर)",
    "Detailed Project Report (DPR) with cash-flow projection": "नकदी प्रवाह अनुमान सहित विस्तृत परियोजना रिपोर्ट (DPR)",
    "Proof of business premises / lease deed": "व्यावसायिक परिसर का प्रमाण / पट्टा विलेख",
    "Bank Account details and ITR / Net worth proof": "बैंक खाते का विवरण और ITR / कुल संपत्ति का प्रमाण",
    "Active Savings Bank Account or Post Office Savings Account": "सक्रिय बचत बैंक खाता या डाकघर बचत खाता",
    "Active Mobile Phone Number": "सक्रिय मोबाइल नंबर",
    "Nominee Details (Aadhaar & Relationship)": "नामांकित व्यक्ति का विवरण (आधार और संबंध)",
    "Bank Account details with auto-debit consent form": "ऑटो-डेबिट सहमति-पत्र सहित बैंक खाते का विवरण",
    "Nominee identification and KYC": "नामांकित व्यक्ति की पहचान और KYC",
    "Birth Certificate of the girl child": "बालिका का जन्म प्रमाणपत्र",
    "Aadhaar Card and PAN of the parent/legal guardian": "माता-पिता/कानूनी अभिभावक का आधार कार्ड और PAN",
    "Address proof of parent/guardian": "माता-पिता/अभिभावक का पता प्रमाण",
    "Passport size photographs of child and guardian": "बालिका और अभिभावक के पासपोर्ट आकार के फोटो",
    "Educational qualification certificate / marksheet": "शैक्षणिक योग्यता प्रमाणपत्र / अंकसूची",
    "Passport size photos": "पासपोर्ट आकार के फोटो",
    "Land Ownership Documents or Registered Lease Agreement for water body": "भूमि स्वामित्व दस्तावेज़ या जलाशय का पंजीकृत पट्टा समझौता",
    "Caste Certificate (for SC/ST availing 60% subsidy)": "जाति प्रमाणपत्र (60% अनुदान लेने वाले SC/ST लाभार्थियों के लिए)",
    "Educational qualification certificates": "शैक्षणिक योग्यता प्रमाणपत्र",
    "Bank Account details (DBT linked)": "बैंक खाते का विवरण (DBT से जुड़ा हुआ)",
    "Uttar Pradesh Domicile / Residence Certificate": "उत्तर प्रदेश का मूल निवास / निवास प्रमाणपत्र",
    "Aadhaar Card of girl child and parents": "बालिका और माता-पिता के आधार कार्ड",
    "Income Certificate issued by Tehsildar": "तहसीलदार द्वारा जारी आय प्रमाणपत्र",
    "Admission proof / School Certificate for relevant stage": "संबंधित चरण के प्रवेश का प्रमाण / विद्यालय प्रमाणपत्र",
    "Joint Bank Account passbook with mother/guardian": "माता/अभिभावक के साथ संयुक्त बैंक खाते की पासबुक",
    "Tamil Nadu Smart Ration Card (Family Card)": "तमिलनाडु स्मार्ट राशन कार्ड (परिवार कार्ड)",
    "Aadhaar Card of female head of family": "परिवार की महिला मुखिया का आधार कार्ड",
    "Electricity consumer number bill receipt": "बिजली उपभोक्ता संख्या वाली बिल रसीद",
    "Rajasthan Bonafide Domicile Certificate (Mool Niwas Praman Patra)": "राजस्थान का मूल निवास प्रमाणपत्र",
    "Graduation Degree Certificate & Final Marksheet": "स्नातक डिग्री प्रमाणपत्र और अंतिम अंकसूची",
    "Income Certificate (Self / Parents)": "स्वयं / माता-पिता का आय प्रमाणपत्र",
    "Aadhaar Card and Jan Aadhaar Card": "आधार कार्ड और जन आधार कार्ड",
    "Bank Account Passbook (Jan Aadhaar seeded)": "बैंक पासबुक (जन आधार से जुड़ी हुई)",
}


def localize_document(value: str, lang: str = "en") -> str:
    if lang != "hi":
        return value
    if value in DOCUMENT_EXACT_HI:
        return DOCUMENT_EXACT_HI[value]
    # Replace longest terms first and keep numbers, official acronyms, and URLs intact.
    for english, hindi in sorted(DOCUMENT_PHRASES_HI.items(), key=lambda pair: len(pair[0]), reverse=True):
        value = value.replace(english, hindi)
    suffixes = {
        " (linked with bank account)": " (बैंक खाते से जुड़ा हुआ)",
        " (DBT-enabled NPCI mapped)": " (DBT सक्षम और NPCI से मैप किया हुआ)",
        " (Aadhaar linked)": " (आधार से जुड़ा हुआ)",
        " (with IFSC and DBT linkage)": " (IFSC और DBT लिंक सहित)",
        " (if applicable)": " (यदि लागू हो)", " (if available)": " (यदि उपलब्ध हो)",
        " (if existing)": " (यदि उपलब्ध हो)", " linked with Aadhaar": " आधार से जुड़ा हुआ",
        " of all family members": " परिवार के सभी सदस्यों के", " of girl child": " बालिका का",
        " of parents/guardian": " माता-पिता/अभिभावक का", " issued by competent revenue authority": " सक्षम राजस्व प्राधिकारी द्वारा जारी",
        " (if applying under SC/ST quota)": " (SC/ST आरक्षण के अंतर्गत आवेदन पर)",
        " (for SC/ST availing 60% subsidy)": " (60% अनुदान लेने वाले SC/ST लाभार्थियों के लिए)",
        " with IFSC and Aadhaar linkage": " IFSC और आधार लिंक सहित",
        " linked with Aadhaar for OTP e-KYC": " OTP ई-KYC के लिए आधार से जुड़ा हुआ",
        " linked with Aadhaar": " आधार से जुड़ा हुआ",
        " with ": " सहित ",
        " or ": " या ",
        " and ": " और ",
        " of ": " का ",
        " for ": " के लिए ",
        " of all family members": " परिवार के सभी सदस्यों के",
        " of parents/guardian": " माता-पिता/अभिभावक का",
        " issued by ": " द्वारा जारी ",
        "Active Mobile number": "सक्रिय मोबाइल नंबर",
        "Active Mobile Number": "सक्रिय मोबाइल नंबर",
        "Urban ": "शहरी ",
        "voter card": "मतदाता पहचान पत्र",
        "Self / Parents": "स्वयं / माता-पिता",
        "marksheet": "अंकसूची",
        "Mool Niwas Praman Patra": "मूल निवास प्रमाणपत्र",
        "ID Card": "पहचान पत्र",
        "ID": "पहचान पत्र",
    }
    for english, hindi in sorted(suffixes.items(), key=lambda pair: len(pair[0]), reverse=True):
        value = value.replace(english, hindi)
    return value


def localize_scheme(scheme: dict, lang: str = "en") -> dict:
    """Return localized presentation fields without changing the underlying record."""
    result = deepcopy(scheme)
    if lang != "hi":
        return result
    scheme_id = result.get("id") or result.get("scheme_id")
    text = SCHEME_TEXT_HI.get(scheme_id)
    if text:
        result["department"], result["category"], result["short_description"], result["benefits"] = text
    if result.get("hindi_name"):
        result["name"] = result["hindi_name"]
        if "scheme_name" in result:
            result["scheme_name"] = result["hindi_name"]
    if result.get("score_disclaimer"):
        result["score_disclaimer"] = "यह आंतरिक स्कोर केवल योजनाओं को क्रमबद्ध करने के लिए है। यह सरकारी स्वीकृति की संभावना या लाभ की गारंटी नहीं दर्शाता।"
    if result.get("required_documents"):
        result["required_documents"] = [localize_document(doc, lang) for doc in result["required_documents"]]
    return result


DOCUMENT_CATEGORY_HI = {
    "Identity & Personal KYC": "पहचान और व्यक्तिगत KYC",
    "Banking & Direct Benefit Transfer (DBT)": "बैंकिंग और प्रत्यक्ष लाभ अंतरण (DBT)",
    "Income, Caste & Social Category": "आय, जाति और सामाजिक श्रेणी",
    "Residence & Domicile Proof": "निवास और मूल निवासी प्रमाण",
    "Occupation, Land, Education & Business Proof": "व्यवसाय, भूमि, शिक्षा और व्यापार प्रमाण",
}

CATEGORY_HI = {
    "Agriculture": "कृषि",
    "Healthcare": "स्वास्थ्य सेवा",
    "Housing": "आवास",
    "Social Welfare & Energy": "सामाजिक कल्याण एवं ऊर्जा",
    "MSME & Business": "सूक्ष्म व्यवसाय एवं उद्यम",
    "Artisans & MSME": "कारीगर एवं MSME",
    "Livelihood & MSME": "आजीविका एवं MSME",
    "Social Assistance & Senior Citizens": "सामाजिक सहायता एवं वरिष्ठ नागरिक",
    "Education & Scholarships": "शिक्षा एवं छात्रवृत्ति",
    "Women & MSME": "महिला एवं MSME",
    "Social Security & Pension": "सामाजिक सुरक्षा एवं पेंशन",
    "Insurance & Social Security": "बीमा एवं सामाजिक सुरक्षा",
    "Women & Child": "महिला एवं बाल कल्याण",
    "Skill Development": "कौशल विकास",
    "Fisheries & Agriculture": "मत्स्य पालन एवं कृषि",
    "Skill & Employment": "कौशल एवं रोजगार",
    "Women Welfare & Social Security": "महिला कल्याण एवं सामाजिक सुरक्षा",
    "Youth & Employment": "युवा एवं रोजगार",
}

PROFILE_VALUE_HI = {
    "farmer": "किसान", "student": "विद्यार्थी", "woman entrepreneur": "महिला उद्यमी",
    "street vendor": "स्ट्रीट वेंडर", "artisan": "कारीगर", "business owner": "व्यवसायी",
    "unemployed": "बेरोजगार", "senior citizen": "वरिष्ठ नागरिक", "employed": "वेतनभोगी कर्मचारी",
    "other": "अन्य", "any": "सभी", "All": "सभी राज्य",
    "Andhra Pradesh": "आंध्र प्रदेश", "Arunachal Pradesh": "अरुणाचल प्रदेश", "Assam": "असम",
    "Bihar": "बिहार", "Chhattisgarh": "छत्तीसगढ़", "Goa": "गोवा", "Gujarat": "गुजरात",
    "Haryana": "हरियाणा", "Himachal Pradesh": "हिमाचल प्रदेश", "Jharkhand": "झारखंड",
    "Karnataka": "कर्नाटक", "Kerala": "केरल", "Madhya Pradesh": "मध्य प्रदेश",
    "Maharashtra": "महाराष्ट्र", "Manipur": "मणिपुर", "Meghalaya": "मेघालय", "Mizoram": "मिजोरम",
    "Nagaland": "नागालैंड", "Odisha": "ओडिशा", "Punjab": "पंजाब", "Rajasthan": "राजस्थान",
    "Sikkim": "सिक्किम", "Tamil Nadu": "तमिलनाडु", "Telangana": "तेलंगाना", "Tripura": "त्रिपुरा",
    "Uttar Pradesh": "उत्तर प्रदेश", "Uttarakhand": "उत्तराखंड", "West Bengal": "पश्चिम बंगाल",
    "Andaman and Nicobar Islands": "अंडमान और निकोबार द्वीपसमूह", "Chandigarh": "चंडीगढ़",
    "Delhi": "दिल्ली", "Jammu and Kashmir": "जम्मू और कश्मीर", "Ladakh": "लद्दाख",
    "Lakshadweep": "लक्षद्वीप", "Puducherry": "पुदुचेरी",
    "Rural": "ग्रामीण", "Urban": "शहरी", "Semi-Urban": "अर्ध-शहरी",
}


def localize_category(value: str, lang: str = "en") -> str:
    return CATEGORY_HI.get(value, value) if lang == "hi" else value


def localize_profile_value(value: str, lang: str = "en") -> str:
    return PROFILE_VALUE_HI.get(value, value) if lang == "hi" else value


RULE_HI = {
    "Geographic Applicability": "भौगोलिक लागूता", "State Domicile": "राज्य का निवास",
    "State Restriction": "राज्य संबंधी शर्त", "Minimum Age": "न्यूनतम आयु",
    "Maximum Age": "अधिकतम आयु", "Age Requirement": "आयु संबंधी शर्त",
    "Age Verification": "आयु सत्यापन", "Annual Family Income": "वार्षिक पारिवारिक आय",
    "Income Ceiling": "आय सीमा", "Income Verification": "आय सत्यापन",
    "Income Requirement": "आय संबंधी शर्त", "Occupation Requirement": "व्यवसाय संबंधी शर्त",
    "Occupation Verification": "व्यवसाय सत्यापन", "Occupation Restriction": "व्यवसाय संबंधी सीमा",
    "Gender Requirement": "लिंग संबंधी शर्त", "Gender Verification": "लिंग सत्यापन",
    "Gender Restriction": "लिंग संबंधी सीमा", "Social Category": "सामाजिक श्रेणी",
    "Social Category Verification": "सामाजिक श्रेणी सत्यापन", "Social Category Restriction": "सामाजिक श्रेणी संबंधी सीमा",
    "Residence Area Match": "निवास क्षेत्र का मिलान", "Residence Verification": "निवास सत्यापन",
    "Residence Restriction": "निवास संबंधी सीमा", "Farmer Status": "किसान स्थिति",
    "Area of Residence": "निवास क्षेत्र", "Cultivable Landholding": "खेती योग्य भूमि",
    "Farmer Requirement": "किसान संबंधी शर्त", "Gender Specificity": "लिंग-विशिष्ट शर्त",
    "Landholding Record": "भूमि स्वामित्व रिकॉर्ड", "LPG Connection Exclusion": "एलपीजी कनेक्शन संबंधी अपात्रता",
    "Pucca House Ownership Exclusion": "पक्का मकान स्वामित्व संबंधी अपात्रता",
    "Residence Applicability": "निवास संबंधी लागूता", "Residence Area Restriction": "निवास क्षेत्र संबंधी सीमा",
    "Social Category Requirement": "सामाजिक श्रेणी संबंधी शर्त", "Student Enrolment": "विद्यार्थी नामांकन",
    "Student Requirement": "विद्यार्थी संबंधी शर्त", "Tax Payer Exclusion": "करदाता संबंधी अपात्रता",
    "Landholding Requirement": "भूमि स्वामित्व संबंधी शर्त", "Student Status": "विद्यार्थी स्थिति",
    "Student Verification": "विद्यार्थी स्थिति सत्यापन", "Income Tax Exclusion": "आयकर संबंधी अपात्रता",
    "No Existing LPG Connection": "पहले से एलपीजी कनेक्शन न होना",
    "No Pucca House Ownership": "पक्का मकान न होना",
}

EXACT_CONDITION_HI = {
    "Open to citizens across all occupations.": "सभी व्यवसायों के नागरिकों के लिए उपलब्ध।",
    "Applicable regardless of gender.": "लिंग की परवाह किए बिना लागू।",
    "Open to all social categories without restriction.": "सभी सामाजिक श्रेणियों के लिए खुली योजना।",
    "Open to both rural and urban residents nationwide.": "देशभर के ग्रामीण और शहरी निवासियों के लिए उपलब्ध।",
    "No strict income ceiling specified under published guidelines.": "प्रकाशित दिशा-निर्देशों में आय की कोई निश्चित अधिकतम सीमा नहीं है।",
    "User is verified as engaged in farming/agriculture.": "कृषि कार्य में संलग्न होना सत्यापित है।",
    "Scheme requires ownership of cultivable landholding.": "योजना के लिए खेती योग्य भूमि का स्वामित्व आवश्यक है।",
    "Scheme requires verified cultivable land title.": "योजना के लिए खेती योग्य भूमि के स्वामित्व का सत्यापन आवश्यक है।",
    "Exclusive to agricultural landholding farmers.": "केवल कृषि भूमि रखने वाले किसानों के लिए।",
    "Scheme requires landholding farmer status.": "योजना के लिए भूमिधारक किसान होना आवश्यक है।",
    "Enrolment in recognized educational institution confirmed.": "मान्यता प्राप्त शिक्षण संस्थान में नामांकन की पुष्टि हुई।",
    "Exclusively for enrolled students.": "केवल नामांकित विद्यार्थियों के लिए।",
    "Scheme requires active enrolment in educational courses.": "योजना के लिए शैक्षणिक पाठ्यक्रम में सक्रिय नामांकन आवश्यक है।",
    "Individuals paying Income Tax are explicitly excluded under scheme rules.": "योजना के नियमों के अनुसार आयकर देने वाले व्यक्ति पात्र नहीं हैं।",
    "Applicant household must not already possess an LPG cylinder connection.": "आवेदक के परिवार के पास पहले से एलपीजी कनेक्शन नहीं होना चाहिए।",
    "Household confirmed as having no prior LPG connection.": "परिवार के पास पहले से एलपीजी कनेक्शन न होने की पुष्टि हुई।",
    "Family should not own a permanent pucca house anywhere in India.": "परिवार के पास भारत में कहीं भी पक्का मकान नहीं होना चाहिए।",
    "Beneficiary family does not own a pucca house.": "लाभार्थी परिवार के पास पक्का मकान नहीं है।",
    "Please specify your state of residence.": "कृपया अपने निवास का राज्य बताएं।",
    "Please provide your age to verify eligibility.": "पात्रता जांचने के लिए कृपया अपनी आयु बताएं।",
    "Please provide a valid numeric income.": "कृपया आय की सही संख्या दर्ज करें।",
    "Please enter your family's annual income.": "कृपया अपने परिवार की वार्षिक आय दर्ज करें।",
    "Please select your primary occupation.": "कृपया अपना मुख्य व्यवसाय चुनें।",
    "Please specify Rural or Urban residence.": "कृपया ग्रामीण या शहरी निवास चुनें।",
    "Select gender if you wish to confirm eligibility for women/gender-specific benefits.": "महिला या लिंग-विशिष्ट लाभों की पात्रता जांचने के लिए अपना लिंग चुनें।",
    "Provide social category if seeking reserved category scholarship or welfare benefits.": "आरक्षित श्रेणी की छात्रवृत्ति या कल्याण लाभ जांचने के लिए अपनी सामाजिक श्रेणी बताएं।",
    "Enter cultivable landholding in hectares.": "खेती योग्य भूमि का क्षेत्रफल हेक्टेयर में दर्ज करें।",
    "Confirm whether you are an enrolled student.": "पुष्टि करें कि आप किसी शिक्षण संस्थान में नामांकित विद्यार्थी हैं या नहीं।",
}


def localize_condition_text(value: str, lang: str = "en") -> str:
    if lang != "hi":
        return value
    if value in EXACT_CONDITION_HI:
        return EXACT_CONDITION_HI[value]
    patterns = [
        (r"Applicable nationwide across all States & UTs \(Scheme Level: Central\)\.", "यह केंद्रीय योजना सभी राज्यों और केंद्र शासित प्रदेशों में लागू है।"),
        (r"Age \((\d+)\) meets minimum age of (\d+) years\.", r"आयु (\1 वर्ष) न्यूनतम आयु (\2 वर्ष) की शर्त पूरी करती है।"),
        (r"Age \((\d+)\) falls within allowed range \((\d+) - (\d+) years\)\.", r"आयु (\1 वर्ष) निर्धारित सीमा (\2–\3 वर्ष) के भीतर है।"),
        (r"Age \((\d+)\) is below minimum requirement of (\d+) years\.", r"आयु (\1 वर्ष) न्यूनतम आवश्यक आयु (\2 वर्ष) से कम है।"),
        (r"Age \((\d+)\) exceeds maximum threshold of (\d+) years\.", r"आयु (\1 वर्ष) अधिकतम सीमा (\2 वर्ष) से अधिक है।"),
        (r"Minimum required age is (\d+) years\.", r"न्यूनतम आवश्यक आयु \1 वर्ष है।"),
        (r"Maximum allowable age is (\d+) years\.", r"अधिकतम अनुमत आयु \1 वर्ष है।"),
        (r"Annual income of ₹([\d,]+) is within ceiling of ₹([\d,]+)\.", r"वार्षिक आय ₹\1, निर्धारित अधिकतम सीमा ₹\2 के भीतर है।"),
        (r"Family income limit is ₹([\d,]+) per annum\.", r"परिवार की वार्षिक आय सीमा ₹\1 है।"),
        (r"Reported income exceeds eligibility ceiling by ₹([\d,]+)\.", r"बताई गई आय पात्रता सीमा से ₹\1 अधिक है।"),
        (r"Scheme has an income threshold of ₹([\d,]+) per year\.", r"योजना की वार्षिक आय सीमा ₹\1 है।"),
        (r"Occupation \((.*?)\) aligns with target beneficiaries\.", r"व्यवसाय (\1) लक्षित लाभार्थियों से मेल खाता है।"),
        (r"Residence \((.*?)\) matches target area\.", r"निवास क्षेत्र (\1) योजना के लक्षित क्षेत्र से मेल खाता है।"),
        (r"Cultivable land record confirmed \((.*?) hectares\)\.", r"खेती योग्य भूमि का रिकॉर्ड सत्यापित है (\1 हेक्टेयर)।"),
    ]
    for pattern, replacement in patterns:
        if re.fullmatch(pattern, value):
            return re.sub(pattern, replacement, value)
    replacements = {
        "Scheme specifies age criteria": "योजना में आयु संबंधी शर्त है",
        " years).": " वर्ष)।", " years.": " वर्ष।", "Age within permissible range": "आयु अनुमत सीमा में है",
        "This state-specific scheme is restricted to:": "यह राज्य-विशिष्ट योजना केवल इस राज्य के लिए है:",
        "User is a resident of ": "आवेदक इस राज्य के निवासी हैं: ",
        "which matches scheme requirements.": "जो योजना की शर्तों से मेल खाता है।",
        "Scheme is restricted to ": "यह योजना केवल इस क्षेत्र के लिए है: ",
        "Resident of ": "इस राज्य के निवासी: ", "is not eligible for this state scheme.": "इस राज्य योजना के लिए पात्र नहीं हैं।",
        "Scheme is targeted to:": "योजना के लक्षित लाभार्थी:",
        "Gender (": "लिंग (", ") matches scheme guidelines.": ") योजना के दिशा-निर्देशों से मेल खाता है।",
        "Social category (": "सामाजिक श्रेणी (", ") matches target reservation.": ") लक्षित आरक्षण से मेल खाती है।",
        "Scheme targets ": "योजना के लक्षित क्षेत्र: ", " areas.": " क्षेत्र।",
        "User residence (": "आवेदक का निवास (", ") is not covered by this scheme.": ") इस योजना में शामिल नहीं है।",
        "Applicant is not an agricultural farmer.": "आवेदक कृषि किसान नहीं हैं।",
    }
    for english, hindi in replacements.items():
        value = value.replace(english, hindi)
    profile_values = {
        "woman entrepreneur": "महिला उद्यमी", "street vendor": "स्ट्रीट वेंडर",
        "business owner": "व्यवसायी", "senior citizen": "वरिष्ठ नागरिक",
        "farmer": "किसान", "student": "विद्यार्थी", "artisan": "कारीगर",
        "unemployed": "बेरोजगार", "employed": "वेतनभोगी कर्मचारी",
        "Rural": "ग्रामीण", "Urban": "शहरी", "Semi-Urban": "अर्ध-शहरी",
        "Female": "महिला", "Male": "पुरुष", "Transgender": "ट्रांसजेंडर",
        "General": "सामान्य", "OBC": "OBC", "Prefer not to say": "बताना नहीं चाहते",
    }
    for english, hindi in profile_values.items():
        value = re.sub(rf"\b{re.escape(english)}\b", hindi, value, flags=re.IGNORECASE)
    return value


def localize_condition(condition: dict, lang: str = "en") -> dict:
    result = deepcopy(condition)
    if lang == "hi":
        result["rule"] = RULE_HI.get(result.get("rule"), result.get("rule"))
        for field in ("detail", "reason", "action"):
            if result.get(field):
                result[field] = localize_condition_text(result[field], lang)
    return result
