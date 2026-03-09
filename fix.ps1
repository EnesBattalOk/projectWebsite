 = Get-Content -Raw templates/water_diary.html

$replacements = @{
    'KATILIMCILAR' = 'PARTICIPANTS'
    'Henüz katılım yok.' = 'No participants yet.'
    'Tüketim Verileri' = 'Consumption Data'
    'Öğrenci Adı Soyadı' = 'Student Full Name'
    'Adınız...' = 'Your Name...'
    'Okul Adı' = 'School Name'
    'Okulunuz...' = 'Your School...'
    'Öğretmen Adı' = 'Teacher Name'
    'Öğretmeniniz...' = 'Your Teacher...'
    'Kişi Sayısı' = 'Family Size'
    'Okul Logosu' = 'School Logo'
    'DÖNEM' = 'PERIOD'
    'TON' = 'TONS'
    'NOT' = 'NOTE'
    'TOPLAM' = 'TOTAL'
    '0.00 Ton' = '0.00 Tons'
    'Analiz Sonuçları' = 'Analysis Results'
    'Aylık Ort.' = 'Monthly Avg.'
    'Kişi Başı' = 'Per Person'
    'WHO Standardı:' = 'WHO Standard:'
    '>Tasarruf Önerileriniz<' = '>Your Saving Suggestions<'
    'Öneriniz 1...' = 'Your Suggestion 1...'
    'Öneriniz 2...' = 'Your Suggestion 2...'
    'id=""cardName"">Öğrenci Adı<' = 'id=""cardName"">Student Name<'
    'id=""cardSchool"">Okul Adı<' = 'id=""cardSchool"">School Name<'
    'Öğretmen:' = 'Teacher:'
    'Toplam Ton' = 'Total Tons'
    'Toplam Litre' = 'Total Liters'
    'L/Günlük' = 'L/Daily'
    'L/Kişi' = 'L/Person'
    'WHO Standardına Uygun!' = 'Meets WHO Standard!'
    'Tasarruf İlkelerim:' = 'My Saving Principles:'
    'Listeye Kaydet' = 'Save to List'
    'Raporu Resim Olarak İndir' = 'Download Report as Image'
    'Ekim / Oct' = 'October'
    'Kasım / Nov' = 'November'
    'Aralık / Dec' = 'December'
    'Veri Bekleniyor' = 'Waiting for Data'
    'Uyumlu' = 'Compliant'
    'WHO Standart Uyumu' = 'WHO Standard Compliance'
    'Standart Dışı' = 'Non-Standard'
    'İsim giriniz!' = 'Please enter a name!'
    'Kaydedildi!' = 'Saved!'
    'Hata oluştu.' = 'An error occurred.'
    '> Kaydet' = '> Save'
    'Su_Gunlugu_' = 'Water_Diary_'
    'Raporu' = 'Report'
}

foreach ($key in $replacements.Keys) {
    $content = $content.Replace($key, $replacements[$key])
}

Set-Content -Path templates/water_diary.html -Value $content -Encoding UTF8

$css = Get-Content -Raw static/css/style.css
$css = $css.Replace('.nav-logo {', "".nav-logo {
    text-decoration: none !important;"")
Set-Content -Path static/css/style.css -Value $css -Encoding UTF8
