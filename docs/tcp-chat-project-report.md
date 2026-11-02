# TCP Chat: Project Report

Hebrew project report with neutral example usernames. [Download the Word document](tcp-chat-project-report.docx).

The report describes the original coursework session. For commands supported by the current checked-in client, see the [README](../README.md#client-commands).

<p dir="rtl">דוח פרויקט: מערכת צ'אט מבוססת Sockets וניתוח תעבורה</p>

<h2 dir="rtl">1. הסבר כללי על המערכת ומבנה הקוד</h2>

<p dir="rtl">המערכת היא מערכת צ'אט רשתית במודל Client-Server המבוסס על פרוטוקול TCP.</p>

<p dir="rtl">המטרה היא לאפשר תקשורת אמינה בזמן אמת בין מספר לקוחות דרך שרת מרכזי שמנהל את ניתוב ההודעות, תוך שימוש בפרוטוקול תקשורת יעיל וממשק שורת פקודה (CLI).</p>

<p dir="rtl">מבנה הקוד:</p>

<p dir="rtl">השרת (Server): השרת הוגדר להאזנה בכתובת 0.0.0.0 (כדי לאפשר חיבור מכל כרטיס רשת) ובפורט 50000. הקוד משתמש ב-Threads (תהליכונים) כדי לטפל במספר לקוחות במקביל. כמו כן, נעשה שימוש במנגנון Locking (threading.Lock) כדי למנוע התנגשויות גישה לזיכרון המשותף (רשימת המשתמשים) ולמנוע קריסות בעת התחברות/התנתקות.</p>

<p dir="rtl">הלקוח (Client): אפליקציית צ'אט בממשק שורת פקודה (Console). הלקוח מריץ שני תהליכים במקביל:</p>

<p dir="rtl">התהליכון הראשי (Main Thread): קולט פקודות מהמשתמש (<code dir="ltr">/all, /dm, /quit</code>) ושולח אותן לשרת לפי הפרוטוקול.</p>

<p dir="rtl">תהליכון ההאזנה (Listening Thread): מאזין כל הזמן להודעות נכנסות. הלקוח מממש מנגנון Buffer חכם שמטפל בבעיית ה-Fragmentation של TCP (מצבים בהם הודעות מגיעות בחלקים או מחוברות), על ידי זיהוי תו ירידת שורה (<code dir="ltr">\n</code>).</p>

<h2 dir="rtl">2. הוראות התקנה והרצה</h2>

<p dir="rtl">הגדרת שרת: הרצת קובץ השרת בסביבת Python. השרת מדפיס הודעה שהוא מאזין בפורט 50000 וממתין לחיבורים.</p>

<p dir="rtl">מציאת IP: בדיקת כתובת ה-IPv4 הפנימית של מחשב השרת (בעזרת פקודת ipconfig בטרמינל). בדוגמה שלנו: 192.168.1.73.</p>

<p dir="rtl">הגדרות אבטחה: הוספת חריגה (Rule) ב-Windows Defender Firewall לפתיחת פורט 50000 בפרוטוקול TCP, כדי לאפשר למחשבים אחרים להתחבר.</p>

<p dir="rtl">חיבור לקוח: הרצת קובץ הלקוח במחשב אחר באותה רשת WiFi. הלקוח מתחבר לכתובת ה-IP של השרת שנמצאה בשלב 2.</p>

<h2 dir="rtl">3. דוגמאות קלט ופלט</h2>

<p dir="rtl">תרחיש לדוגמה: משתמש בשם Alice מתחבר, שולח הודעה לכולם, ואז שולח הודעה פרטית למשתמש Bob.</p>

<p dir="rtl">קלט בלקוח (Client Input):</p>

<p dir="rtl">הזנת שם משתמש: Alice</p>

<p dir="rtl">שליחת הודעה לכולם: <code dir="ltr">/all Hello everyone</code></p>

<p dir="rtl">שליחת הודעה פרטית: <code dir="ltr">dm Bob are you ready?</code></p>

<p dir="rtl">יציאה: /quit</p>

<p dir="rtl">פלט בשרת (Server Log):</p>

<pre dir="ltr"><code>[*] New physical connection from ('192.168.1.82', 64512)
[LOGIN] User 'Alice' connected
[CHAT - GROUP] Alice: Hello everyone
[CHAT - PRIVATE] Alice to Bob: Are you ready?
[LOGOUT] User 'Alice' disconnected.</code></pre>

<p dir="rtl">פלט במסך הלקוח (Client Output):</p>

<pre dir="ltr"><code>Connected to server
SYS WELCOME
OK Logged in as Alice
MSG GROUP Charlie: Hi Alice!
MSG DM Bob: Yes I am ready.</code></pre>

<h2 dir="rtl">4. ניתוח תעבורה (Wireshark)</h2>

<p dir="rtl">הניטור בוצע על גבי ממשק ה-WiFi כדי ללכוד תעבורה בין שני מחשבים שונים ברשת.</p>

<p dir="rtl">שכבת הרשת (IPv4): זיהינו את חבילות ה-IP העוברות בין כתובת השרת (192.168.1.73) לבין כתובת הלקוח.</p>

<p dir="rtl">שכבת התעבורה (TCP):</p>

<p dir="rtl">לחיצת יד משולשת (Three-way Handshake): זיהוי תהליך הקמת הקשר (SYN, SYN-ACK, ACK) מול פורט היעד 50000.</p>

<p dir="rtl">דגלים (Flags): שימוש בדגל PSH (Push) המעיד על העברת נתונים מיידית (הודעות הצ'אט) ללא המתנה ב-Buffer.</p>

<p dir="rtl">שכבת היישום (Payload): צפייה בתוכן ההודעות הגולמי כפי שהוגדר בפרוטוקול הטקסטואלי שבנינו (למשל: <code dir="ltr">LOGIN Alice\n</code> או <code dir="ltr">ALL Hello\n</code>).</p>

<h2 dir="rtl">5. תיאור שימוש בבינה מלאכותית (AI)</h2>

<p dir="rtl">א. מטרות השימוש</p>

<p dir="rtl">ה-AI שימש ככלי עזר טכני ("Copilot") ויועץ לפיתוח. המטרות כללו המרה של הקוד לממשק CLI יציב, פתרון בעיות תקשורת רשת (חסימות Firewall), ותכנון לוגיקה למניעת איבוד הודעות ברשת.</p>

<p dir="rtl">ב. דוגמאות לפרומפטים :</p>

<p dir="rtl">"איך אני מתקן מצב שבו הודעות נדבקות אחת לשנייה ב-TCP כשאני שולח אותן מהר?" (פתרון: שימוש ב-Buffer והפרדה לפי <code dir="ltr">\n</code>).</p>

<p dir="rtl">"ה-Ping עובד אבל ה-Python לא מתחבר, מה יכולה להיות הבעיה?" (פתרון: הוספת חריגה ב-Firewall לפורט 50000).</p>

<p dir="rtl">"איך לממש פקודות כמו /dm ו-/all בצורה יעילה בתוך הלקוח?"</p>

<p dir="rtl">"איך להגן על השרת מקריסה כשמשתמש מתנתק בפתאומיות?" (פתרון: שימוש ב-try/except וניקוי רשימת המשתמשים בצורה בטוחה).</p>
