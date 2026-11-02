# TCP Chat: Project Report

Browser-readable transcription of the original Hebrew report. [Download the Word document](tcp-chat-project-report.docx).

The report describes the original coursework session. For commands supported by the current checked-in client, see the [README](../README.md#client-commands).

<div dir="rtl">

דוח פרויקט: מערכת צ'אט מבוססת Sockets וניתוח תעבורה

## 1. הסבר כללי על המערכת ומבנה הקוד

המערכת היא מערכת צ'אט רשתית במודל Client-Server המבוסס על פרוטוקול TCP.

המטרה היא לאפשר תקשורת אמינה בזמן אמת בין מספר לקוחות דרך שרת מרכזי שמנהל את ניתוב ההודעות, תוך שימוש בפרוטוקול תקשורת יעיל וממשק שורת פקודה (CLI).

מבנה הקוד:

השרת (Server): השרת הוגדר להאזנה בכתובת 0.0.0.0 (כדי לאפשר חיבור מכל כרטיס רשת) ובפורט 50000. הקוד משתמש ב-Threads (תהליכונים) כדי לטפל במספר לקוחות במקביל. כמו כן, נעשה שימוש במנגנון Locking (threading.Lock) כדי למנוע התנגשויות גישה לזיכרון המשותף (רשימת המשתמשים) ולמנוע קריסות בעת התחברות/התנתקות.

הלקוח (Client): אפליקציית צ'אט בממשק שורת פקודה (Console). הלקוח מריץ שני תהליכים במקביל:

Main Thread: קולט פקודות מהמשתמש (/all, /dm, /quit) ושולח אותן לשרת לפי הפרוטוקול.

Listening Thread: מאזין כל הזמן להודעות נכנסות. הלקוח מממש מנגנון Buffer חכם שמטפל בבעיית ה-Fragmentation של TCP (מצבים בהם הודעות מגיעות בחלקים או מחוברות), על ידי זיהוי תו ירידת שורה (\n).

## 2. הוראות התקנה והרצה

הגדרת שרת: הרצת קובץ השרת בסביבת Python. השרת מדפיס הודעה שהוא מאזין בפורט 50000 וממתין לחיבורים.

מציאת IP: בדיקת כתובת ה-IPv4 הפנימית של מחשב השרת (בעזרת פקודת ipconfig בטרמינל). בדוגמה שלנו: 192.168.1.73.

הגדרות אבטחה: הוספת חריגה (Rule) ב-Windows Defender Firewall לפתיחת פורט 50000 בפרוטוקול TCP, כדי לאפשר למחשבים אחרים להתחבר.

חיבור לקוח: הרצת קובץ הלקוח במחשב אחר באותה רשת WiFi. הלקוח מתחבר לכתובת ה-IP של השרת שנמצאה בשלב 2.

## 3. דוגמאות קלט ופלט

תרחיש לדוגמה: משתמש בשם shaked מתחבר, שולח הודעה לכולם, ואז שולח הודעה פרטית למשתמש omer.

קלט בלקוח (Client Input):

הזנת שם משתמש: shaked

שליחת הודעה לכולם: /all Hello everyone

שליחת הודעה פרטית: dm omer are you ready?

יציאה: /quit

פלט בשרת (Server Log):

Plaintext

[*] New physical connection from ('192.168.1.82', 64512)

[LOGIN] User 'Shaked' connected

[CHAT - GROUP] Shaked: Hello everyone

[CHAT - PRIVATE] Shaked to omer: Are you ready?

[LOGOUT] User 'Shaked' disconnected.

פלט במסך הלקוח (Client Output):

Plaintext

Connected to server

SYS WELCOME

OK Logged in as Shaked

MSG GROUP Nir: Hi Shaked!

MSG DM Omer: Yes I am ready.

## 4. ניתוח תעבורה (Wireshark)

הניטור בוצע על גבי ממשק ה-WiFi כדי ללכוד תעבורה בין שני מחשבים שונים ברשת.

שכבת הרשת (IPv4): זיהינו את חבילות ה-IP העוברות בין כתובת השרת (192.168.1.73) לבין כתובת הלקוח.

שכבת התעבורה (TCP):

Three-way Handshake: זיהוי תהליך הקמת הקשר (SYN, SYN-ACK, ACK) מול פורט היעד 50000.

Flags: שימוש בדגל PSH (Push) המעיד על העברת נתונים מיידית (הודעות הצ'אט) ללא המתנה ב-Buffer.

שכבת היישום (Payload): צפייה בתוכן ההודעות הגולמי כפי שהוגדר בפרוטוקול הטקסטואלי שבנינו (למשל: LOGIN Shaked\n או ALL Hello\n).

## 5. תיאור שימוש בבינה מלאכותית (AI)

א. מטרות השימוש

ה-AI שימש ככלי עזר טכני ("Copilot") ויועץ לפיתוח. המטרות כללו המרה של הקוד לממשק CLI יציב, פתרון בעיות תקשורת רשת (חסימות Firewall), ותכנון לוגיקה למניעת איבוד הודעות ברשת.

ב. דוגמאות לפרומפטים :

"איך אני מתקן מצב שבו הודעות נדבקות אחת לשנייה ב-TCP כשאני שולח אותן מהר?" (פתרון: שימוש ב-Buffer והפרדה לפי \n).

"ה-Ping עובד אבל ה-Python לא מתחבר, מה יכולה להיות הבעיה?" (פתרון: הוספת חריגה ב-Firewall לפורט 50000).

"איך לממש פקודות כמו /dm ו-/all בצורה יעילה בתוך הלקוח?"

"איך להגן על השרת מקריסה כשמשתמש מתנתק בפתאומיות?" (פתרון: שימוש ב-try/except וניקוי רשימת המשתמשים בצורה בטוחה).

</div>
