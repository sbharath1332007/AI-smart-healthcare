"""
AI Smart Healthcare - Clinical Knowledge Base
Comprehensive medical condition database, symptom patterns, diet protocols, and lifestyle medicine.
"""

EMERGENCY_RED_FLAGS = [
    {
        "id": "cardiac_emergency",
        "triggers": ["crushing chest pain", "chest tightness radiating to arm", "chest pressure jaw", "sudden cold sweat chest"],
        "condition": "Suspected Acute Coronary Syndrome / Heart Attack",
        "action": "IMMEDIATE EMERGENCY: Call 911 / 112 / Emergency Services immediately. Do not drive yourself. Rest in a seated position."
    },
    {
        "id": "stroke_emergency",
        "triggers": ["sudden facial drooping", "one side arm weakness", "slurred speech", "sudden vision loss one eye", "sudden confusion"],
        "condition": "Suspected Cerebrovascular Accident (Stroke)",
        "action": "IMMEDIATE EMERGENCY: Act F.A.S.T. (Face, Arms, Speech, Time). Call emergency services immediately. Note the exact time symptoms started."
    },
    {
        "id": "anaphylaxis_emergency",
        "triggers": ["throat swelling", "difficulty swallowing breathing", "swollen lips tongue wheezing", "severe allergic reaction"],
        "condition": "Suspected Anaphylactic Reaction",
        "action": "IMMEDIATE EMERGENCY: Administer Epinephrine Auto-Injector (EpiPen) if available. Call emergency services immediately."
    },
    {
        "id": "respiratory_emergency",
        "triggers": ["severe shortness of breath", "unable to speak full sentences", "blue lips", "cyanosis", "gasping for air"],
        "condition": "Acute Severe Respiratory Failure",
        "action": "IMMEDIATE EMERGENCY: Call emergency services immediately. Sit upright, administer prescribed rescue inhaler or supplemental oxygen if available."
    },
    {
        "id": "severe_headache_emergency",
        "triggers": ["thunderclap headache", "worst headache of my life", "sudden explosive head pain with stiff neck"],
        "condition": "Suspected Subarachnoid Hemorrhage / Meningitis",
        "action": "IMMEDIATE EMERGENCY: Proceed to the nearest Emergency Department immediately. Avoid taking blood thinners."
    }
]

CONDITIONS_DB = [
    {
        "id": "gerd",
        "name": "Gastroesophageal Reflux Disease (GERD) & Acid Reflux",
        "category": "Gastroenterology",
        "urgency": "Routine",
        "specialist": "Gastroenterologist",
        "symptoms": {
            "heartburn": 3.0,
            "acid regurgitation": 3.0,
            "chest burning": 2.5,
            "sour taste in mouth": 2.5,
            "bloating": 1.5,
            "difficulty swallowing": 1.5,
            "chronic dry cough": 1.5,
            "throat clearing": 1.2,
            "nausea after meals": 1.5,
            "burning in upper stomach": 2.0
        },
        "explanation": (
            "Gastroesophageal Reflux Disease (GERD) occurs when the lower esophageal sphincter (LES)—the muscular "
            "valve separating your esophagus and stomach—relaxes abnormally or weakens. This allows acidic stomach "
            "juices and digestive enzymes to flow backward into the esophagus. Over time, the acidic wash irritates "
            "and inflames the sensitive esophageal lining, causing burning pain (heartburn), sour regurgitation, and "
            "sometimes throat irritation or coughing."
        ),
        "solutions": [
            "Schedule an evaluation with a primary care physician or Gastroenterologist if symptoms occur more than twice weekly.",
            "Use approved over-the-counter antacids (calcium carbonate) for immediate temporary relief, or H2 blockers/PPIs as guided by your doctor.",
            "Avoid lying down, bending over, or reclining for at least 3 hours following any meal.",
            "Elevate the head of your bed by 6 to 8 inches using bed risers or a firm wedge pillow.",
            "Avoid tight-fitting waistbands or belts that increase intra-abdominal pressure.",
            "Seek immediate emergency care if chest pain radiates to your left shoulder, arm, or jaw, or is accompanied by shortness of breath."
        ],
        "diet": {
            "guideline": "Low-acid, anti-reflux Mediterranean-style diet with smaller, frequent meals.",
            "foods_to_eat": [
                "Oatmeal, whole wheat bread, brown rice, and quinoa",
                "Non-citrus fruits: bananas, melons, apples, and pears",
                "Lean poultry, white fish, tofu, and egg whites",
                "Green vegetables: broccoli, asparagus, spinach, kale, zucchini, cucumbers",
                "Healthy fats in moderation: avocado, extra virgin olive oil, almonds",
                "Ginger tea, chamomile tea, and alkaline water"
            ],
            "foods_to_avoid": [
                "Spicy foods, chili peppers, hot sauces",
                "Tomatoes, tomato sauce, pizza sauce, ketchup",
                "Citrus fruits: oranges, grapefruits, lemons, limes",
                "Chocolate, spearmint, peppermint",
                "Caffeinated beverages (coffee, energy drinks) and carbonated sodas",
                "Fried, greasy, or deep-fried fast food",
                "Alcohol and smoking"
            ],
            "meal_timing": "Eat 4-5 smaller meals instead of 2-3 heavy meals. Complete dinner at least 3-4 hours prior to sleeping.",
            "hydration": "Drink water between meals rather than large quantities during meals to prevent stomach distension."
        },
        "lifestyle": {
            "exercise": "Engage in moderate low-impact activities like brisk walking, stationary cycling, or light yoga. Avoid heavy crunches or strenuous inversions right after eating.",
            "sleep": "Sleep predominantly on your left side; anatomically, left-side sleeping keeps the gastric junction above gastric acid levels. Use a wedge pillow.",
            "stress_management": "Chronic stress amplifies pain perception in the esophageal nerves. Practice diaphragmatic breathing, box breathing (4-4-4-4), and progressive muscle relaxation.",
            "habits": "Cease cigarette smoking and vaping, as nicotine directly relaxes the lower esophageal sphincter."
        }
    },
    {
        "id": "hypertension",
        "name": "Elevated Blood Pressure & Essential Hypertension",
        "category": "Cardiovascular",
        "urgency": "Urgent",
        "specialist": "Cardiologist or Primary Care Physician",
        "symptoms": {
            "headache in back of head": 2.5,
            "dizziness": 2.0,
            "shortness of breath": 2.2,
            "palpitations": 2.0,
            "fatigue": 1.5,
            "blurred vision": 2.2,
            "flushing": 1.2,
            "nosebleeds": 1.5,
            "chest tightness": 2.5,
            "pulsing sensation in neck or ears": 2.2
        },
        "explanation": (
            "Hypertension (high blood pressure) is a chronic medical condition where the force of the blood flowing "
            "against your artery walls is consistently too high (typically systolic >= 130 mmHg or diastolic >= 80 mmHg). "
            "It is often referred to as a 'silent killer' because it may cause few overt symptoms early on, but gradually "
            "damages the vascular endothelium, increasing strain on the heart, kidneys, and cerebrovascular vessels."
        ),
        "solutions": [
            "Check and record your blood pressure twice daily (morning and evening) with a validated home arm cuff.",
            "Consult a physician promptly for comprehensive cardiovascular screening (ECG, lipid panel, kidney function).",
            "If your blood pressure exceeds 180/120 mmHg or you experience sudden severe headache or chest pain, seek immediate emergency care (Hypertensive Crisis).",
            "Take prescribed antihypertensive medications (ACE inhibitors, ARBs, Calcium Channel Blockers) consistently without skipping doses.",
            "Work with your doctor on a gradual cardiovascular conditioning program."
        ],
        "diet": {
            "guideline": "Strict DASH Diet (Dietary Approaches to Stop Hypertension), rich in potassium, magnesium, and fiber.",
            "foods_to_eat": [
                "Potassium-rich foods: sweet potatoes, bananas, spinach, white beans, avocados",
                "Magnesium sources: pumpkin seeds, chia seeds, almonds, dark leafy greens",
                "Flaxseeds and walnuts rich in omega-3 fatty acids",
                "Garlic, berries (blueberries, strawberries rich in anthocyanins), and beets (natural nitrates)",
                "Low-fat unsweetened Greek yogurt and skim milk",
                "Whole grains: steel-cut oats, buckwheat, quinoa"
            ],
            "foods_to_avoid": [
                "Excess dietary sodium: aim for < 1,500 mg - 2,000 mg of sodium per day",
                "Processed deli meats, canned soups, frozen ready-to-eat meals, soy sauce",
                "Trans fats, saturated fats, processed commercial pastries",
                "Excessive caffeine and energy drinks",
                "Alcohol (limit to zero or strictly under guidelines)"
            ],
            "meal_timing": "Balanced meals with consistent electrolyte distribution. Never skip breakfast.",
            "hydration": "Maintain 2.5 to 3 liters of filtered water daily to assist renal sodium excretion."
        },
        "lifestyle": {
            "exercise": "Aim for at least 150 minutes of moderate-intensity aerobic exercise per week (brisk walking, swimming, light cycling). Avoid sudden heavy isometric weightlifting without medical clearance.",
            "sleep": "Ensure 7 to 9 hours of uninterrupted restorative sleep. Screen for obstructive sleep apnea (OSA) if you snore heavily.",
            "stress_management": "Engage in daily mindfulness meditation, biofeedback, or 15 minutes of slow rhythmic breathing (6 breaths per minute).",
            "habits": "Completely quit smoking; nicotine causes immediate vasoconstriction and chronic arterial stiffening."
        }
    },
    {
        "id": "type2_diabetes",
        "name": "Type 2 Diabetes Mellitus & Insulin Resistance",
        "category": "Endocrinology",
        "urgency": "Urgent",
        "specialist": "Endocrinologist",
        "symptoms": {
            "excessive thirst": 3.0,
            "frequent urination": 3.0,
            "increased hunger": 2.5,
            "unexplained weight loss": 2.2,
            "chronic fatigue": 2.0,
            "blurry vision": 2.0,
            "tingling in feet or hands": 2.5,
            "slow healing sores": 2.5,
            "frequent infections": 2.0,
            "dry mouth": 1.8
        },
        "explanation": (
            "Type 2 Diabetes develops when cells in muscle, fat, and the liver become resistant to insulin—the hormone "
            "secreted by pancreatic beta cells that shuttles glucose into cells for fuel. Over time, the pancreas cannot "
            "keep up with the demand, leading to persistent hyperglycemia (elevated blood sugar). Chronic high glucose levels "
            "damage blood vessels and nerves throughout the body."
        ),
        "solutions": [
            "Undergo formal laboratory screening: Fasting Plasma Glucose, HbA1c, and Oral Glucose Tolerance Test.",
            "Establish regular self-monitoring of blood glucose (SMBG) or continuous glucose monitoring (CGM).",
            "Coordinate with an endocrinologist and a certified diabetes care and education specialist (CDCES).",
            "Inspect feet daily for cuts, blisters, redness, or ulcers due to reduced peripheral sensation.",
            "Attend annual dilated eye exams and renal function panels (eGFR, microalbuminuria)."
        ],
        "diet": {
            "guideline": "Low-Glycemic Index (GI), high-fiber, macronutrient-balanced nutrition plan.",
            "foods_to_eat": [
                "Non-starchy vegetables: broccoli, cauliflower, green beans, bell peppers, leafy greens",
                "Complex fiber-rich carbohydrates: lentils, chickpeas, black beans, steel-cut oats",
                "High-quality proteins: wild salmon, organic eggs, grilled chicken breast, edamame",
                "Healthy monounsaturated fats: extra virgin olive oil, walnuts, chia seeds",
                "Low-glycemic fruits in moderation: blueberries, blackberries, raspberries, green apples",
                "Cinnamon, apple cider vinegar (prior to meals), green tea"
            ],
            "foods_to_avoid": [
                "Refined carbohydrates: white bread, refined white pasta, white rice, pastries",
                "Sugar-sweetened beverages: sodas, sweetened iced teas, fruit juices",
                "Added sugars, high-fructose corn syrup, candy, sugary cereals",
                "Trans fats and fried fast foods"
            ],
            "meal_timing": "Consistent meal timing; pair all carbohydrates with lean protein and fiber to blunt postprandial glucose spikes.",
            "hydration": "Drink water generously throughout the day (3 liters); avoid sweetened sports drinks."
        },
        "lifestyle": {
            "exercise": "Combine resistance training (2-3 days/week) with aerobic exercise (150 mins/week). Muscle contraction pulls glucose from blood independent of insulin.",
            "sleep": "Maintain 7-8 hours of sleep; sleep deprivation spikes cortisol and worsens insulin resistance.",
            "stress_management": "Chronic stress releases epinephrine and cortisol, driving up blood glucose. Use yoga, nature walks, and journaling.",
            "habits": "Take a 10-15 minute walk immediately after each meal to markedly reduce post-meal blood sugar surges."
        }
    },
    {
        "id": "migraine",
        "name": "Migraine Headache with or without Aura",
        "category": "Neurology",
        "urgency": "Routine",
        "specialist": "Neurologist",
        "symptoms": {
            "throbbing headache": 3.0,
            "one sided head pain": 3.0,
            "sensitivity to light": 3.0,
            "sensitivity to sound": 2.8,
            "nausea": 2.5,
            "visual aura or flashing lights": 3.0,
            "vomiting": 2.0,
            "worse with movement": 2.2,
            "neck stiffness": 1.8,
            "fatigue before headache": 1.5
        },
        "explanation": (
            "Migraine is a complex neurovascular disorder characterized by recurrent, pulsating, moderate-to-severe "
            "headaches, frequently unilateral. It stems from neurogenic inflammation and hyperexcitability of the "
            "trigeminovascular system, causing release of neuropeptides like CGRP (calcitonin gene-related peptide) and "
            "transient cortical spreading depression (which causes visual auras)."
        ),
        "solutions": [
            "Rest immediately in a dark, quiet, temperature-controlled room at the earliest onset of symptoms.",
            "Apply a cold compress or ice pack wrapped in a cloth to your forehead or the back of your neck.",
            "Consult a neurologist regarding abortive medications (Triptans, CGRP receptor antagonists) and preventive therapies.",
            "Keep a detailed headache diary recording triggers, sleep duration, foods, and weather changes.",
            "Seek emergency care if you experience a sudden explosive 'thunderclap' headache or neurological deficits (weakness, numbness, speech changes)."
        ],
        "diet": {
            "guideline": "Anti-inflammatory, trigger-free whole food diet with regular hydration.",
            "foods_to_eat": [
                "Magnesium-rich foods: almonds, spinach, pumpkin seeds, black beans",
                "Riboflavin (Vitamin B2) sources: eggs, mushrooms, lean poultry",
                "Omega-3 fatty acids: salmon, sardines, walnuts to reduce neuroinflammation",
                "Hydrating foods: cucumbers, watermelon, celery",
                "Ginger (natural anti-nausea and anti-inflammatory properties)"
            ],
            "foods_to_avoid": [
                "Aged cheeses (cheddar, parmesan, blue cheese containing tyramine)",
                "Processed meats with nitrates/nitrites (bacon, hot dogs, salami)",
                "Artificial sweeteners (aspartame, sucralose)",
                "Monosodium glutamate (MSG) and heavy processed snacks",
                "Red wine, beer, and fermented alcoholic beverages",
                "Skipping meals or fasting intermittently without preparation"
            ],
            "meal_timing": "Never skip meals; hypoglycemia is a potent migraine trigger. Eat at consistent intervals.",
            "hydration": "Drink 2.5 to 3 liters of water daily. Dehydration is a primary trigger."
        },
        "lifestyle": {
            "exercise": "Regular low-intensity cardiovascular exercise (walking, swimming) on non-headache days. Avoid abrupt high-intensity workouts without warming up.",
            "sleep": "Strict sleep schedule: go to bed and wake up at the exact same hour daily, including weekends.",
            "stress_management": "Biofeedback, progressive muscle relaxation, and cognitive behavioral therapy (CBT) for stress reduction.",
            "habits": "Limit blue light and screen exposure; use blue-light blocking lenses and take frequent screen breaks."
        }
    },
    {
        "id": "asthma",
        "name": "Bronchial Asthma & Hyperreactive Airway Disease",
        "category": "Pulmonology",
        "urgency": "Urgent",
        "specialist": "Pulmonologist / Allergist",
        "symptoms": {
            "wheezing": 3.0,
            "shortness of breath": 3.0,
            "chest tightness": 2.5,
            "cough worse at night": 2.8,
            "cough with exercise": 2.5,
            "rapid breathing": 2.2,
            "difficulty catching breath": 2.8,
            "mucus production": 1.5,
            "allergic reaction triggers": 2.0
        },
        "explanation": (
            "Asthma is a chronic inflammatory condition of the airways (bronchial tubes) characterized by recurrent "
            "episodes of airway hyperresponsiveness, reversible bronchospasm, and excessive mucus secretion. Triggers such "
            "as allergens, viral respiratory infections, cold dry air, exercise, or smoke cause smooth muscle constriction "
            "and mucosal edema, narrowing the passages through which oxygen reaches the alveoli."
        ),
        "solutions": [
            "Follow your Asthma Action Plan: use prescribed rescue bronchodilators (e.g., Albuterol/Salbutamol) immediately during acute flare-ups.",
            "Use daily inhaled corticosteroids (controller inhalers) exactly as prescribed to keep chronic inflammation controlled.",
            "Schedule spirometry and pulmonary function tests with a pulmonologist.",
            "Avoid known personal triggers: tobacco smoke, dust mites, pet dander, mold, and cold drafts.",
            "Call emergency services immediately if rescue inhaler provides no relief, lips turn blue, or you cannot complete full sentences."
        ],
        "diet": {
            "guideline": "Anti-inflammatory, antioxidant-rich diet supporting respiratory immune function.",
            "foods_to_eat": [
                "Vitamin C & E rich fruits and vegetables: bell peppers, kiwi, oranges, broccoli, sunflower seeds",
                "Omega-3 fatty acids: wild-caught oily fish (salmon, mackerel) to lower leukotriene production",
                "Vitamin D sources: fortified milk, egg yolks, safe morning sunlight exposure",
                "Magnesium sources: leafy greens, legumes, whole grains (magnesium relaxes bronchial smooth muscles)",
                "Turmeric and ginger for natural anti-inflammatory benefits"
            ],
            "foods_to_avoid": [
                "Foods containing sulfites (dried fruit, wine, pickled goods, shrimp)",
                "Excessive cold beverages or ice creams that may induce reflexive airway spasm in sensitive individuals",
                "Highly processed foods containing artificial food dyes and preservatives",
                "Heavy dairy products if they exacerbate phlegm sensation"
            ],
            "meal_timing": "Eat light, manageable portions; large heavy meals push up on the diaphragm, restricting lung expansion.",
            "hydration": "Warm herbal teas, broths, and room-temperature water to keep airway secretions thin and easy to clear."
        },
        "lifestyle": {
            "exercise": "Warm up thoroughly for 10-15 minutes prior to exercise. Choose asthma-friendly exercises like swimming in humid environments or brisk walking.",
            "sleep": "Use hypoallergenic, dust-mite-proof pillowcases and mattress encasings. Maintain bedroom humidity between 30% and 50%.",
            "stress_management": "Practice diaphragmatic breathing and Buteyko breathing techniques under clinical supervision.",
            "habits": "Install a HEPA air purifier in your bedroom; never permit indoor smoking or vaping."
        }
    },
    {
        "id": "generalized_anxiety",
        "name": "Generalized Anxiety Disorder (GAD) & Autonomic Hyperarousal",
        "category": "Psychiatry / Mental Health",
        "urgency": "Routine",
        "specialist": "Psychiatrist or Clinical Psychologist",
        "symptoms": {
            "excessive worry": 3.0,
            "restlessness": 2.5,
            "rapid heartbeat": 2.5,
            "muscle tension": 2.2,
            "trouble sleeping": 2.5,
            "fatigue": 2.0,
            "difficulty concentrating": 2.2,
            "irritability": 2.0,
            "sweating or trembling": 2.2,
            "shortness of breath with panic": 2.5,
            "nervous stomach or nausea": 2.0
        },
        "explanation": (
            "Generalized Anxiety Disorder and chronic anxiety states involve persistent, excessive, and uncontrollable "
            "worry regarding everyday events. Physiologically, it is driven by dysregulation in the amygdala and prefrontal cortex "
            "and chronic hyperactivity of the sympathetic nervous system (fight-or-flight), leading to excess adrenaline and "
            "cortisol, tachycardia, muscle bracing, and visceral hypersensitivity."
        ),
        "solutions": [
            "Consult a licensed mental health professional for Cognitive Behavioral Therapy (CBT), the gold standard evidence-based treatment.",
            "Explore medically guided therapies (SSRIs, SNRIs) if anxiety significantly impairs daily functioning.",
            "Practice the 4-7-8 breathing technique: inhale for 4 seconds, hold for 7 seconds, exhale slowly for 8 seconds to stimulate the vagus nerve.",
            "Use the 5-4-3-2-1 sensory grounding exercise during acute panic or overwhelming anxiety.",
            "Rule out somatic contributors with your doctor: thyroid dysfunction, caffeine toxicity, or cardiac arrhythmias."
        ],
        "diet": {
            "guideline": "Neuro-supportive, blood-sugar stabilizing diet rich in gut-brain axis nutrients.",
            "foods_to_eat": [
                "Fermented probiotic foods: kefir, Greek yogurt, kimchi, sauerkraut (supports serotonin production in the gut)",
                "Complex carbs: sweet potatoes, whole oats, brown rice (steady tryptophan absorption)",
                "Magnesium & zinc: pumpkin seeds, cashews, spinach, oysters",
                "Omega-3 fatty acids: salmon, chia seeds, flaxseed oil",
                "Herbal infusions: chamomile, lemon balm, ashwagandha, passionflower tea"
            ],
            "foods_to_avoid": [
                "High doses of caffeine, pre-workout supplements, energy drinks",
                "Refined sugars and high-glycemic snacks that trigger blood sugar crashes and adrenaline surges",
                "Alcohol (produces rebound anxiety during metabolism and disrupts REM sleep)",
                "Artificial additives and high-sodium processed foods"
            ],
            "meal_timing": "Eat regular, predictable meals every 3-4 hours to prevent reactive hypoglycemia-induced panic.",
            "hydration": "Drink at least 2.5 liters of water; mild dehydration triggers physiologic stress responses and tachycardia."
        },
        "lifestyle": {
            "exercise": "Engage in 30 minutes of rhythmic aerobic exercise (jogging, cycling, dancing) to metabolize stress hormones and release endorphins.",
            "sleep": "Strict digital detox 60 minutes before bed. Keep bedroom cool (65°F / 18°C) and completely dark.",
            "stress_management": "Daily 15-minute mindfulness meditation (using apps like Headspace or Insight Timer) and physiological sigh breathing.",
            "habits": "Limit exposure to distressing news media and social media feeds."
        }
    },
    {
        "id": "ibs",
        "name": "Irritable Bowel Syndrome (IBS)",
        "category": "Gastroenterology",
        "urgency": "Routine",
        "specialist": "Gastroenterologist",
        "symptoms": {
            "abdominal cramping": 3.0,
            "bloating": 3.0,
            "gas": 2.5,
            "alternating diarrhea and constipation": 3.0,
            "diarrhea after eating": 2.8,
            "mucus in stool": 2.2,
            "feeling of incomplete evacuation": 2.2,
            "abdominal pain relieved by bowel movement": 2.8
        },
        "explanation": (
            "Irritable Bowel Syndrome (IBS) is a common disorder of the gut-brain interaction. It involves abnormal "
            "gastrointestinal motility, visceral hypersensitivity (the gut nerves perceive normal digestion as painful), "
            "altered intestinal microbiome composition, and microscopic immune activation, without structural tissue destruction."
        ),
        "solutions": [
            "Consult a gastroenterologist to rule out inflammatory bowel disease (Crohn's, Ulcerative Colitis) and celiac disease.",
            "Try a structured, short-term Low-FODMAP diet under the supervision of a registered dietitian.",
            "Consider antispasmodics, soluble fiber supplements (psyllium husk), or gut-targeted probiotics as advised by your physician.",
            "Track symptoms alongside food and stress logs to pinpoint individual trigger foods.",
            "Seek immediate medical attention if you experience rectal bleeding, unexplained weight loss, or persistent nocturnal diarrhea."
        ],
        "diet": {
            "guideline": "Low-FODMAP (Fermentable Oligosaccharides, Disaccharides, Monosaccharides, and Polyols) elimination and reintroduction plan.",
            "foods_to_eat": [
                "Gluten-free grains: rice, quinoa, gluten-free oats",
                "Vegetables: carrots, cucumbers, zucchini, bell peppers, spinach",
                "Fruits: blueberries, strawberries, oranges, cantaloupe",
                "Proteins: chicken, turkey, fish, eggs, firm tofu",
                "Lactose-free milk, almond milk, hard cheeses (parmesan, cheddar)",
                "Peppermint tea (natural smooth-muscle antispasmodic)"
            ],
            "foods_to_avoid": [
                "High-FODMAP foods: garlic, onions, shallots, leeks",
                "Legumes, kidney beans, baked beans, lentils",
                "Wheat, rye, and barley products",
                "High-fructose fruits: apples, pears, mangoes, watermelons",
                "Artificial sweeteners containing polyols (sorbitol, mannitol, xylitol)",
                "Carbonated beverages and chewing gum"
            ],
            "meal_timing": "Chew food thoroughly, eat in a relaxed unhurried environment, and avoid oversized meals.",
            "hydration": "Sip room-temperature water steadily; avoid drinking through straws to reduce swallowed air."
        },
        "lifestyle": {
            "exercise": "Regular gentle physical activity such as brisk walking, pilates, and restorative yoga promotes healthy colon transit.",
            "sleep": "Ensure 7-8 hours of sleep; circadian rhythm disruption directly disrupts intestinal peristalsis.",
            "stress_management": "Gut-directed hypnotherapy, mindfulness meditation, and deep abdominal breathing help down-regulate the enteric nervous system.",
            "habits": "Establish a consistent daily bathroom routine, allowing comfortable unhurried time each morning."
        }
    },
    {
        "id": "osteoarthritis",
        "name": "Osteoarthritis & Degenerative Joint Disease",
        "category": "Rheumatology / Orthopedics",
        "urgency": "Routine",
        "specialist": "Orthopedic Specialist / Rheumatologist",
        "symptoms": {
            "joint pain": 3.0,
            "joint stiffness in morning": 2.5,
            "stiffness after resting": 2.5,
            "cracking or popping in joints": 2.2,
            "reduced range of motion": 2.2,
            "swelling around joint": 2.0,
            "bone tenderness": 2.0,
            "joint pain worse with weather change": 1.8
        },
        "explanation": (
            "Osteoarthritis is the most prevalent form of arthritis, characterized by progressive breakdown and loss "
            "of articular cartilage capping the ends of bones within synovial joints. As the protective cartilage cushion "
            "thins, bone-on-bone friction develops, causing subchondral bone remodeling, bone spurs (osteophytes), low-grade "
            "synovial inflammation, pain, and loss of joint mobility."
        ),
        "solutions": [
            "Consult an orthopedic specialist or physical therapist for customized joint-stabilizing rehabilitation.",
            "Use topical nonsteroidal anti-inflammatory gels (e.g., Voltaren / Diclofenac) or oral options under medical supervision.",
            "Apply heat packs before movement to relieve morning stiffness; apply cold packs after activity to reduce swelling.",
            "Maintain an optimal body weight to decrease mechanical load on weight-bearing joints (knees, hips, spine).",
            "Discuss joint protection braces, ergonomic footwear, and assistive devices with an occupational therapist."
        ],
        "diet": {
            "guideline": "Anti-inflammatory Mediterranean nutritional framework supporting cartilage and joint health.",
            "foods_to_eat": [
                "Fatty fish rich in EPA and DHA: wild salmon, sardines, trout, mackerel",
                "Extra virgin olive oil (contains oleocanthal, a natural anti-inflammatory agent)",
                "Deep colored berries: cherries, blackberries, blueberries (rich in anthocyanins)",
                "Cruciferous vegetables: broccoli, Brussels sprouts, cabbage (rich in sulforaphane)",
                "Bone broth, collagen peptides, and Vitamin C-rich foods (citrus, bell peppers)",
                "Turmeric / Curcumin paired with black pepper (piperine)"
            ],
            "foods_to_avoid": [
                "Refined sugars and high-fructose corn syrup that fuel systemic inflammatory cytokine cascades",
                "Processed meats and foods rich in advanced glycation end-products (AGEs)",
                "Trans fats and hydrogenated cooking oils",
                "Excessive alcohol consumption"
            ],
            "meal_timing": "Nutrient-dense regular meals with adequate protein to preserve joint-supporting muscle mass.",
            "hydration": "Drink 2 to 3 liters of water; articular cartilage is approximately 80% water and requires hydration to maintain shock-absorbing elasticity."
        },
        "lifestyle": {
            "exercise": "Focus on low-impact joint-friendly conditioning: swimming, water aerobics, stationary cycling, and resistance band strengthening.",
            "sleep": "Use supportive pillows between the knees (side sleepers) or under the knees (back sleepers) to maintain neutral spinal and hip alignment.",
            "stress_management": "Chronic pain increases central sensitization; practice guided imagery, progressive relaxation, and gentle stretching.",
            "habits": "Wear supportive, well-cushioned shock-absorbing footwear; avoid walking barefoot on hard tile or hardwood floors."
        }
    },
    {
        "id": "acute_bronchitis",
        "name": "Acute Bronchitis & Viral Upper/Lower Respiratory Infection",
        "category": "Pulmonology",
        "urgency": "Routine",
        "specialist": "Primary Care Physician",
        "symptoms": {
            "persistent productive cough": 3.0,
            "clear or yellow mucus": 2.5,
            "chest discomfort with coughing": 2.5,
            "low grade fever": 2.0,
            "fatigue": 2.0,
            "sore throat": 1.8,
            "runny nose": 1.5,
            "mild wheezing or shortness of breath": 2.0,
            "body aches": 1.5
        },
        "explanation": (
            "Acute bronchitis is an inflammation of the lining of the bronchial tubes, which carry air to and from your "
            "lungs. Over 90% of cases are caused by common respiratory viruses (such as rhinovirus, adenovirus, influenza, or RSV). "
            "The viral invasion triggers mucosal edema and hypersecretion of mucus, resulting in a persistent hacking cough "
            "that can last 2 to 3 weeks even after the virus is cleared."
        ),
        "solutions": [
            "Rest adequately; allow your immune system to mount an effective antiviral defense.",
            "Use a cool-mist humidifier or take hot steamy showers to loosen bronchial secretions.",
            "Honey (1-2 teaspoons for adults and children over 1 year) is clinically proven to suppress cough frequency and severity.",
            "Avoid requesting antibiotics for viral bronchitis; antibiotics do not kill viruses and cause unnecessary side effects.",
            "Seek urgent medical evaluation if you develop high fever (>102°F / 38.9°C), cough up blood, or experience severe shortness of breath."
        ],
        "diet": {
            "guideline": "Immune-boosting, warming, nutrient-dense broths and hydration.",
            "foods_to_eat": [
                "Warm bone broths and chicken vegetable soup (cysteine in chicken thins mucus)",
                "Warm herbal teas: thyme tea, elderberry, ginger with raw honey and lemon",
                "Garlic, onions, and horseradish for natural antimicrobials",
                "Vitamin C rich fruits: kiwi, oranges, papaya, strawberries",
                "Easily digestible meals: steamed sweet potatoes, brown rice, soft poached eggs"
            ],
            "foods_to_avoid": [
                "Dairy products if they make your phlegm feel thicker",
                "Cold drinks and sugary beverages",
                "Processed, salty snacks and heavy greasy foods",
                "Alcohol and caffeine which dehydrate mucous membranes"
            ],
            "meal_timing": "Small, light, comforting meals whenever appetite permits.",
            "hydration": "Drink at least 3 liters of warm fluids daily to keep mucosal secretions thin and easily expectorated."
        },
        "lifestyle": {
            "exercise": "Strict rest during acute fever and coughing spells. Gentle indoor walking only once fever has resolved for 24 hours.",
            "sleep": "Elevate your head and torso with extra pillows to prevent post-nasal drip from triggering nocturnal cough fits.",
            "stress_management": "Conserve physical and mental energy; practice calming rest and light reading.",
            "habits": "Avoid secondhand tobacco smoke, wood-burning stoves, chemical cleaning sprays, and cold dry outdoor air."
        }
    },
    {
        "id": "urinary_tract_infection",
        "name": "Acute Urinary Tract Infection (Cystitis)",
        "category": "Urology / Nephrology",
        "urgency": "Urgent",
        "specialist": "Primary Care Physician / Urologist",
        "symptoms": {
            "burning sensation when urinating": 3.0,
            "frequent urge to urinate": 3.0,
            "passing frequent small amounts of urine": 2.8,
            "cloudy urine": 2.5,
            "strong smelling urine": 2.2,
            "pelvic pain or lower belly pressure": 2.5,
            "blood in urine": 2.8,
            "low grade fever": 1.8
        },
        "explanation": (
            "A urinary tract infection (UTI) occurs when bacteria (most commonly uropathogenic Escherichia coli) enter "
            "the urinary tract through the urethra and multiply in the bladder (cystitis). The bacterial colonization damages "
            "the urothelial barrier, causing intense local inflammation, painful spasms, and dysuria."
        ),
        "solutions": [
            "Visit a healthcare clinic for a urinalysis and urine culture test to identify the specific pathogen.",
            "Take the complete course of prescribed antibiotics (e.g., Nitrofurantoin, Fosfomycin, Trimethoprim) without stopping early.",
            "Consider over-the-counter Phenazopyridine (Azo) for 1-2 days to relieve acute urinary burning while antibiotics take effect.",
            "Apply a warm heating pad to your lower abdomen to ease bladder spasms.",
            "Seek immediate emergency care if you experience flank/back pain, high fever, chills, or vomiting (signs of kidney infection / pyelonephritis)."
        ],
        "diet": {
            "guideline": "Bladder-friendly hydration and natural urinary tract health support.",
            "foods_to_eat": [
                "Pure unsweetened cranberry juice or D-Mannose supplements (inhibits E. coli adhesion to urothelium)",
                "Probiotic-rich yogurt and kefir to support healthy urogenital flora",
                "Antioxidant-rich berries and vitamin C from bell peppers",
                "Water-dense vegetables: cucumbers, celery, zucchini",
                "Mild herbal teas (corn silk, marshmallow root tea)"
            ],
            "foods_to_avoid": [
                "Caffeine, coffee, black tea, energy drinks",
                "Alcohol, carbonated sodas, artificial sweeteners",
                "Highly spicy foods and acidic citrus juices during active infection",
                "High-sugar desserts and candy"
            ],
            "meal_timing": "Light, wholesome, unprocessed meals.",
            "hydration": "Drink copious amounts of plain water (3 to 3.5 liters daily) to mechanically flush bacteria from the urinary bladder."
        },
        "lifestyle": {
            "exercise": "Rest during acute infection. Avoid high-impact bouncing or bicycle saddles that put pressure on the perineum.",
            "sleep": "Ensure adequate restful sleep; urinate immediately when you feel the urge, never hold urine.",
            "stress_management": "Warm baths (plain water, no bubble bath chemicals or fragrances) and gentle resting.",
            "habits": "Wipe strictly from front to back after using the toilet; urinate promptly after sexual intercourse; wear loose breathable cotton underwear."
        }
    }
]
