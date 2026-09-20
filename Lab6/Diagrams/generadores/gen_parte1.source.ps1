$isLegacyWindowsPowerShell = $PSVersionTable.PSVersion.Major -lt 6
if ($isLegacyWindowsPowerShell -and $env:LAB6_UTF8_BOOTSTRAPPED -ne '1') {
    $env:LAB6_UTF8_BOOTSTRAPPED = '1'
    $env:LAB6_DIAGRAM_GENERATOR_ROOT = $PSScriptRoot
    $utf8Source = [System.IO.File]::ReadAllText(
        $MyInvocation.MyCommand.Path,
        [System.Text.Encoding]::UTF8
    )
    Invoke-Expression $utf8Source
    exit
}

$ErrorActionPreference = 'Stop'
$elements = [System.Collections.ArrayList]::new()
$timestamp = 1725494400000
$lineHeight = 1.25

$BLUE = '#1971c2'
$BLUE_FILL = '#d0ebff'
$PURPLE = '#6741d9'
$PURPLE_FILL = '#ede9fe'
$TEAL = '#0c8599'
$GREEN_FILL = '#d3f9d8'
$ORANGE = '#e67700'
$YELLOW_FILL = '#fff3bf'
$RED = '#c92a2a'
$RED_FILL = '#fff5f5'
$OK = '#2f9e44'
$OK_FILL = '#ebfbee'
$GRAY = '#868e96'
$LIGHT_GRAY = '#ced4da'
$INK = '#1e1e1e'
$BODY = '#3f3f46'
$WHITE = '#ffffff'

function Add-Common {
    param([System.Collections.IDictionary]$Element)
    $Element.seed = 1
    $Element.updated = $timestamp
    $Element.link = $null
    $Element.locked = $false
    $Element.angle = 0
    $Element.opacity = 100
    $Element.groupIds = @()
    $Element.boundElements = @()
    $Element.fillStyle = 'solid'
    if (-not $Element.Contains('backgroundColor')) {
        $Element.backgroundColor = 'transparent'
    }
    $Element.id = $Element.type.Substring(0, 1) + $elements.Count
    [void]$elements.Add([pscustomobject]$Element)
}

function Add-Rect {
    param($X, $Y, $W, $H, $Stroke, $Fill = 'transparent', [switch]$Dashed,
          $Rough = 1, $StrokeWidth = 2)
    Add-Common ([ordered]@{
        type = 'rectangle'; x = $X; y = $Y; width = $W; height = $H
        strokeColor = $Stroke; backgroundColor = $Fill; strokeWidth = $StrokeWidth
        strokeStyle = $(if ($Dashed) { 'dashed' } else { 'solid' })
        roughness = $Rough; roundness = @{ type = 3 }
    })
}

function Add-Ellipse {
    param($X, $Y, $W, $H, $Stroke, $Fill = 'transparent', $StrokeWidth = 2)
    Add-Common ([ordered]@{
        type = 'ellipse'; x = $X; y = $Y; width = $W; height = $H
        strokeColor = $Stroke; backgroundColor = $Fill; strokeWidth = $StrokeWidth
        strokeStyle = 'solid'; roughness = 1; roundness = @{ type = 2 }
    })
}

function Add-DiamondShape {
    param($X, $Y, $W, $H, $Stroke, $Fill)
    Add-Common ([ordered]@{
        type = 'diamond'; x = $X; y = $Y; width = $W; height = $H
        strokeColor = $Stroke; backgroundColor = $Fill; strokeWidth = 2
        strokeStyle = 'solid'; roughness = 1; roundness = @{ type = 2 }
    })
}

function Add-Text {
    param($X, $Y, [string]$Value, $Size = 13, $Color = '#1e1e1e',
          $Align = 'left', $Width = $null, $Family = 1)
    $lines = @($Value -split "`n")
    if ($null -eq $Width) {
        $maxLength = ($lines | ForEach-Object { $_.Length } | Measure-Object -Maximum).Maximum
        $factor = $(if ($Family -eq 3) { 0.60 } else { 0.56 })
        $Width = [Math]::Ceiling($maxLength * $Size * $factor) + 8
    }
    Add-Common ([ordered]@{
        type = 'text'; x = $X; y = $Y; width = $Width
        height = $lines.Count * $Size * $lineHeight; strokeColor = $Color
        strokeWidth = 1; strokeStyle = 'solid'; roughness = 1; roundness = $null
        text = $Value; fontSize = $Size; fontFamily = $Family
        textAlign = $Align; verticalAlign = 'top'; baseline = $Size
        containerId = $null; originalText = $Value; lineHeight = $lineHeight
    })
}

function Add-Path {
    param([string]$Path, $Color = '#495057', $StrokeWidth = 2,
          [switch]$Dashed, [switch]$Arrow)
    $absolutePoints = [System.Collections.ArrayList]::new()
    foreach ($pair in ($Path -split ';')) {
        $parts = $pair -split ','
        [void]$absolutePoints.Add([pscustomobject]@{
            X = [double]$parts[0]
            Y = [double]$parts[1]
        })
    }
    $xs = @($absolutePoints | ForEach-Object { $_.X })
    $ys = @($absolutePoints | ForEach-Object { $_.Y })
    $minX = ($xs | Measure-Object -Minimum).Minimum
    $maxX = ($xs | Measure-Object -Maximum).Maximum
    $minY = ($ys | Measure-Object -Minimum).Minimum
    $maxY = ($ys | Measure-Object -Maximum).Maximum
    $relative = @()
    foreach ($point in $absolutePoints) {
        $relative += ,@(($point.X - $minX), ($point.Y - $minY))
    }
    Add-Common ([ordered]@{
        type = $(if ($Arrow) { 'arrow' } else { 'line' })
        x = $minX; y = $minY; width = $maxX - $minX; height = $maxY - $minY
        strokeColor = $Color; strokeWidth = $StrokeWidth
        strokeStyle = $(if ($Dashed) { 'dashed' } else { 'solid' })
        roughness = 1; roundness = @{ type = 2 }; points = $relative
        lastCommittedPoint = $null; startBinding = $null; endBinding = $null
        startArrowhead = $null; endArrowhead = $(if ($Arrow) { 'arrow' } else { $null })
    })
}

function Add-Arrow {
    param([string]$Path, $Color = '#495057', [switch]$Dashed, $StrokeWidth = 2)
    Add-Path $Path $Color $StrokeWidth -Dashed:$Dashed -Arrow
}

function Add-Zone {
    param($X, $Y, $W, $H, [string]$Title, [string]$Subtitle)
    Add-Rect $X $Y $W $H $LIGHT_GRAY 'transparent' -Dashed -Rough 0 -StrokeWidth 1
    Add-Text ($X + 18) ($Y + 12) $Title 18 $BLUE 'left' ($W - 36) 3
    Add-Text ($X + 18) ($Y + 40) $Subtitle 11 $GRAY 'left' ($W - 36)
}

function Add-Box {
    param($X, $Y, $W, $H, $Stroke, $Fill, [string]$Title,
          [string]$Subtitle = '', $TitleSize = 13, [switch]$Dashed)
    Add-Rect $X $Y $W $H $Stroke $Fill -Dashed:$Dashed
    $titleLines = @($Title -split "`n").Count
    $subLines = $(if ([string]::IsNullOrWhiteSpace($Subtitle)) { 0 } else { @($Subtitle -split "`n").Count })
    $titleHeight = $titleLines * $TitleSize * $lineHeight
    $subHeight = $subLines * 9 * $lineHeight
    $top = $Y + ($H - $titleHeight - $subHeight - $(if ($subLines) { 5 } else { 0 })) / 2
    Add-Text $X $top $Title $TitleSize $Stroke 'center' $W
    if ($subLines) {
        Add-Text $X ($top + $titleHeight + 5) $Subtitle 9 $BODY 'center' $W
    }
}

function Add-Service {
    param($X, $Y, $W, $H, [string]$Name, [string]$Purpose = '')
    Add-Box $X $Y $W $H $BLUE $BLUE_FILL $Name $Purpose 13
}

function Add-ControlService {
    param($X, $Y, $W, $H, [string]$Name, [string]$Purpose = '')
    Add-Box $X $Y $W $H $PURPLE $PURPLE_FILL $Name $Purpose 13
}

function Add-Api {
    param($X, $Y, $W, $H, [string]$Name, [string]$Purpose = '')
    Add-Box $X $Y $W $H $ORANGE $YELLOW_FILL $Name $Purpose 13 -Dashed
}

function Add-Database {
    param($X, $Y, $W, $H, [string]$Name, [string]$Contents = '')
    Add-Ellipse $X $Y $W $H $TEAL $GREEN_FILL
    $titleHeight = @($Name -split "`n").Count * 12 * $lineHeight
    $subHeight = $(if ([string]::IsNullOrWhiteSpace($Contents)) { 0 } else { @($Contents -split "`n").Count * 9 * $lineHeight })
    $top = $Y + ($H - $titleHeight - $subHeight - 3) / 2
    Add-Text $X $top $Name 12 $TEAL 'center' $W
    if ($subHeight) {
        Add-Text $X ($top + $titleHeight + 3) $Contents 9 $BODY 'center' $W
    }
}

function Add-Decision {
    param($X, $Y, $W, $H, [string]$Title)
    Add-DiamondShape $X $Y $W $H $PURPLE $PURPLE_FILL
    $lines = @($Title -split "`n").Count
    $top = $Y + ($H - $lines * 11 * $lineHeight) / 2
    Add-Text $X $top $Title 11 $PURPLE 'center' $W
}

function Add-Terminal {
    param($X, $Y, $W, $H, [string]$Title, $Color = '#2f9e44')
    $fill = $(if ($Color -eq $RED) { $RED_FILL } else { $OK_FILL })
    Add-Ellipse $X $Y $W $H $Color $fill
    $lines = @($Title -split "`n").Count
    $top = $Y + ($H - $lines * 12 * $lineHeight) / 2
    Add-Text $X $top $Title 12 $Color 'center' $W
}

function Add-Outcome {
    param($X, $Y, $W, $H, [string]$Title)
    Add-Box $X $Y $W $H $RED $RED_FILL $Title '' 10 -Dashed
}

function Add-Actor {
    param($X, $Y, [string]$Role)
    Add-Ellipse ($X + 25) $Y 30 30 $BLUE $BLUE_FILL 2
    Add-Path "$($X + 40),$($Y + 30);$($X + 40),$($Y + 72)" $BLUE 2
    Add-Path "$($X + 18),$($Y + 48);$($X + 40),$($Y + 40);$($X + 62),$($Y + 48)" $BLUE 2
    Add-Path "$($X + 40),$($Y + 72);$($X + 22),$($Y + 96)" $BLUE 2
    Add-Path "$($X + 40),$($Y + 72);$($X + 58),$($Y + 96)" $BLUE 2
    Add-Text ($X - 30) ($Y + 102) $Role 11 $BLUE 'center' 140
}

function Add-CallLabel {
    param($X, $Y, [string]$Text, $Color = '#868e96', $Width = 150)
    Add-Text $X $Y $Text 9 $Color 'center' $Width 3
}

# ---------------------------------------------------------------------------
# MARCOS: la lectura es de arriba hacia abajo y aumenta el nivel de detalle.
# ---------------------------------------------------------------------------
Add-Zone 40 170 2820 380 'ITERACIÓN #1 · CONTEXTO' 'Quién participa y cuál es el sistema que coordina el leasing.'
Add-Zone 40 580 2820 560 'ITERACIÓN #2 · ACCESO, REGISTRO Y VALIDACIÓN' 'Se ve el primer WRITE: la empresa pasa de PENDING a VALIDATED.'
Add-Zone 40 1170 2820 600 'ITERACIÓN #3 · SOLICITUD Y PREAPROBACIÓN' 'La solicitud se guarda antes de consultar proveedor, presupuesto y ranking.'
Add-Zone 40 1800 2820 850 'ITERACIÓN #4 · APROBACIONES, CONTRATO, ORDEN Y ENTREGA' 'Cada actor aparece junto al servicio que usa; cada decisión y persistencia es visible.'
Add-Zone 40 2680 2820 1840 'ITERACIÓN #5 · ARQUITECTURA E2E CONSOLIDADA' 'Todo el recorrido en una sola vista: acceso, registro, solicitud, aprobaciones, contrato, orden, entrega y cierre. Aún sin escalar.'

# ---------------------------------------------------------------------------
# CONECTORES (se dibujan primero para que queden detrás de los nodos).
# ---------------------------------------------------------------------------
# Iteración 1
Add-Arrow '560,310;1250,355' $BLUE
Add-Arrow '930,450;1250,390' $BLUE
Add-Arrow '1800,250;1550,325' $BLUE
Add-Arrow '2050,350;1550,355' $BLUE
Add-Arrow '1800,460;1550,385' $BLUE

# Iteración 2 · flujo principal
Add-Arrow '150,770;230,780' $BLUE
Add-Arrow '410,780;470,780' $OK
Add-Arrow '670,780;740,780' $OK
Add-Arrow '960,780;1020,780' $OK
Add-Arrow '1180,780;1250,780' $OK
Add-Arrow '1450,780;1520,780' $OK
Add-Arrow '1720,780;1790,780' $OK
Add-Arrow '1990,780;2090,780' $OK
Add-Arrow '2170,780;2310,780' $OK
# Seguridad y bases
Add-Arrow '320,820;320,900' $PURPLE
Add-Arrow '410,940;480,940' $TEAL
Add-Arrow '570,820;570,875;1350,875;1350,900' $TEAL
Add-Arrow '850,820;850,900' $ORANGE
Add-Arrow '900,820;1050,900' $ORANGE
Add-Arrow '1350,820;1350,900' $TEAL
# Rama NO
Add-Arrow '1100,835;1100,1020' $RED
Add-Arrow '1210,1060;1740,1060;1740,820;1790,820' $RED

# Iteración 3 · flujo principal
Add-Arrow '150,1370;230,1370' $BLUE
Add-Arrow '430,1370;470,1370' $OK
Add-Arrow '670,1370;700,1370' $OK
Add-Arrow '860,1370;900,1370' $OK
Add-Arrow '1100,1370;1130,1370' $OK
Add-Arrow '1290,1370;1330,1370' $OK
Add-Arrow '1530,1370;1570,1370' $OK
Add-Arrow '1770,1370;1810,1370' $OK
Add-Arrow '2010,1370;2050,1370' $OK
Add-Arrow '2250,1370;2320,1370' $OK
Add-Arrow '2400,1370;2500,1370' $OK
# Datos e integraciones
Add-Arrow '330,1410;330,1510' $TEAL
Add-Arrow '570,1410;570,1510' $ORANGE
Add-Arrow '1000,1410;1000,1510' $TEAL
Add-Arrow '1430,1410;1430,1510' $TEAL
Add-Arrow '1670,1410;1670,1510' $TEAL
# Ramas NO
Add-Arrow '780,1425;780,1640' $RED
Add-Arrow '1210,1425;1210,1640' $RED

# Iteración 4 · actores sobre sus decisiones
Add-Arrow '365,1925;365,1965' $BLUE
Add-Arrow '595,1925;595,1965' $BLUE
Add-Arrow '825,1925;825,1965' $BLUE
Add-Arrow '1525,1925;1525,1965' $BLUE
Add-Arrow '1950,1925;2000,1980' $BLUE
Add-Arrow '2465,1925;2465,1965' $BLUE
# Happy path principal
Add-Arrow '230,2020;280,2020' $OK
Add-Arrow '450,2020;510,2020' $OK
Add-Arrow '680,2020;740,2020' $OK
Add-Arrow '910,2020;970,2020' $OK
Add-Arrow '1160,2020;1210,2020' $OK
Add-Arrow '1390,2020;1440,2020' $OK
Add-Arrow '1610,2020;1670,2020' $OK
Add-Arrow '1860,2020;1910,2020' $OK
Add-Arrow '2090,2020;2150,2020' $OK
Add-Arrow '2330,2020;2380,2020' $OK
Add-Arrow '2550,2020;2610,2020' $OK
# Ramas NO
Add-Arrow '365,2075;365,2140' $RED
Add-Arrow '595,2075;595,2140' $RED
Add-Arrow '825,2075;825,2140' $RED
Add-Arrow '1525,2075;1525,2140' $RED
Add-Arrow '2465,2075;2465,2140' $RED
# Persistencia por etapa
Add-Arrow '335,2075;250,2075;250,2315;300,2315' $TEAL -Dashed
Add-Arrow '565,2075;500,2075;500,2315;530,2315' $TEAL -Dashed
Add-Arrow '795,2075;730,2075;730,2315;760,2315' $TEAL -Dashed
Add-Arrow '1065,2060;1065,2280' $TEAL
Add-Arrow '1300,2060;1300,2280' $TEAL
Add-Arrow '1525,2075;1525,2280' $TEAL -Dashed
Add-Arrow '1765,2060;1765,2250;1980,2250;1980,2280' $ORANGE
Add-Arrow '2000,2060;2000,2280' $ORANGE
Add-Arrow '2240,2060;2240,2280' $TEAL
Add-Arrow '2465,2075;2465,2250;2240,2250;2240,2280' $TEAL -Dashed
# Servicios transversales conectados al flujo de negocio
Add-Arrow '1065,2362;1065,2400;535,2400;535,2430' $TEAL -Dashed
Add-Arrow '640,2470;690,2470' $PURPLE
Add-Arrow '870,2470;920,2470' $TEAL
Add-Arrow '1140,2470;1180,2470' $TEAL
Add-Arrow '1340,2470;1390,2470' $RED
Add-Arrow '1610,2470;1660,2470' $ORANGE
Add-Arrow '1840,2470;1920,2470' $ORANGE

# Iteración 5 · entrada única, sin balanceador ni réplicas
Add-Arrow '150,2840;220,2840' $BLUE
Add-Arrow '400,2840;450,2840' $OK
Add-Arrow '650,2840;700,2840' $OK
Add-Arrow '920,2840;920,2960;200,2960;200,3000' $OK

# Fila A · acceso, registro y validación
Add-Arrow '280,3040;310,3040' $OK
Add-Arrow '480,3040;510,3040' $OK
Add-Arrow '700,3040;730,3040' $OK
Add-Arrow '930,3040;960,3040' $OK
Add-Arrow '1110,3040;1150,3040' $OK
Add-Arrow '1350,3040;1390,3040' $OK
Add-Arrow '1035,3095;1035,3120' $RED

# Fila B · solicitud y preaprobación
Add-Arrow '290,3250;320,3250' $OK
Add-Arrow '500,3250;530,3250' $OK
Add-Arrow '680,3250;710,3250' $OK
Add-Arrow '900,3250;930,3250' $OK
Add-Arrow '1080,3250;1110,3250' $OK
Add-Arrow '1300,3250;1330,3250' $OK
Add-Arrow '1540,3250;1580,3250' $OK
Add-Arrow '605,3305;605,3330' $RED
Add-Arrow '1005,3305;1005,3330' $RED

# Continuidad A → B
Add-Arrow '1590,3040;1740,3040;1740,3160;205,3160;205,3210' $OK

# Fila C · aprobaciones y contrato
Add-Arrow '200,3580;230,3580' $OK
Add-Arrow '390,3580;430,3580' $OK
Add-Arrow '610,3580;650,3580' $OK
Add-Arrow '830,3580;870,3580' $OK
Add-Arrow '1050,3580;1090,3580' $OK
Add-Arrow '1270,3580;1310,3580' $OK
Add-Arrow '1500,3580;1540,3580' $OK
Add-Arrow '1740,3580;1780,3580' $OK
Add-Arrow '310,3635;310,3670' $RED
Add-Arrow '520,3635;520,3670' $RED
Add-Arrow '740,3635;740,3670' $RED
Add-Arrow '1405,3635;1405,3670' $RED

# Continuidad B → C
Add-Arrow '1760,3250;2170,3250;2170,3410;125,3410;125,3550' $OK

# Fila D · compra, entrega y conformidad
Add-Arrow '310,3930;350,3930' $OK
Add-Arrow '540,3930;580,3930' $OK
Add-Arrow '770,3930;810,3930' $OK
Add-Arrow '990,3930;1030,3930' $OK
Add-Arrow '900,3985;900,4020' $RED

# Continuidad C → D
Add-Arrow '1970,3580;2450,3580;2450,3860;215,3860;215,3890' $OK

# Una sola infraestructura lógica para toda la iteración
Add-Arrow '280,4210;330,4210' $PURPLE
Add-Arrow '520,4210;570,4210' $PURPLE
Add-Arrow '850,4210;900,4210' $TEAL
Add-Arrow '1060,4210;1110,4210' $RED
Add-Arrow '1330,4210;1370,4210' $ORANGE
Add-Arrow '1560,4210;1610,4210' $ORANGE

# Todos los cambios de estado alimentan el mismo flujo transaccional
Add-Arrow '1250,3080;1250,4120;190,4120;190,4170' $TEAL -Dashed
Add-Arrow '1450,3290;1450,4110;190,4110;190,4170' $TEAL -Dashed
Add-Arrow '1650,3620;1650,4100;190,4100;190,4170' $TEAL -Dashed
Add-Arrow '1130,3970;1130,4090;190,4090;190,4170' $TEAL -Dashed
Add-Arrow '1035,3180;1035,4080;190,4080;190,4170' $RED -Dashed
Add-Arrow '605,3390;605,4070;190,4070;190,4170' $RED -Dashed

# Documentos e integraciones externas
Add-Arrow '825,3000;825,2920;2380,2920;2380,3020' $ORANGE -Dashed
Add-Arrow '410,3210;410,3180;2380,3180;2380,3020' $ORANGE -Dashed
Add-Arrow '445,3970;445,4100;2690,4100;2690,3030;2580,3030' $ORANGE -Dashed
Add-Arrow '1435,3290;1435,4130;2070,4130;2070,4170' $TEAL -Dashed
Add-Arrow '1180,3620;1180,4140;2070,4140;2070,4170' $TEAL -Dashed
Add-Arrow '675,3970;675,4150;2070,4150;2070,4170' $TEAL -Dashed

# ---------------------------------------------------------------------------
# CABECERA Y LEYENDA
# ---------------------------------------------------------------------------
Add-Text 55 35 'TOP DOWN DESIGN · LEA$E' 28 $BLUE 'left' 700 3
Add-Text 55 78 'Del contexto a la arquitectura end-to-end completa · cada iteración agrega detalle verificable' 14 $GRAY 'left' 1000
Add-Text 55 112 'Los *Services* son módulos lógicos del mismo despliegue; no son microservicios independientes.' 11 $BODY 'left' 930

Add-Box 1860 45 170 55 $BLUE $BLUE_FILL 'Service' 'componente interno' 11
Add-Box 2050 45 170 55 $ORANGE $YELLOW_FILL 'API externa' 'dependencia' 11 -Dashed
Add-Database 2240 43 190 58 'DB / Store' 'READ · WRITE'
Add-Decision 2450 43 150 60 '¿decisión?'
Add-Terminal 2620 45 190 55 'ESTADO / FIN' $OK

# ---------------------------------------------------------------------------
# ITERACIÓN 1 · CONTEXTO
# ---------------------------------------------------------------------------
Add-Actor 500 260 'Empresa cliente'
Add-Actor 850 400 'Proveedor'
Add-Actor 1800 200 'Gerente de Ventas'
Add-Actor 2050 300 'Gerente de Logística'
Add-Actor 1800 410 'Gerente de Finanzas'
Add-Box 1250 300 300 110 $BLUE $BLUE_FILL 'Lea$e App' 'coordina solicitud, contrato, compra y entrega' 20
Add-CallLabel 920 310 'solicita leasing' $BLUE 220
Add-CallLabel 1010 430 'confirma disponibilidad y entrega' $BLUE 250
Add-CallLabel 1560 250 'aprueba orden' $BLUE 190
Add-CallLabel 1590 340 'aprueba proveedor y plazo' $BLUE 220
Add-CallLabel 1580 430 'aprueba cuotas y cobro' $BLUE 220

# ---------------------------------------------------------------------------
# ITERACIÓN 2 · LOGIN, REGISTRO, VALIDACIÓN Y PRIMER GUARDADO
# ---------------------------------------------------------------------------
Add-Actor 70 720 'Empresa cliente'
Add-Service 230 740 180 80 'LoginService' 'inicia sesión'
Add-Service 470 740 200 80 'RegisterCompanyService' 'RUC · razón social'
Add-ControlService 740 740 220 80 'CompanyValidationService' 'orquesta las validaciones'
Add-Decision 1020 725 160 110 "¿SUNAT e`nhistorial OK?"
Add-Service 1250 740 200 80 'CompanyProfileService' 'marca VALIDATED'
Add-Service 1520 740 200 80 'NotificationService' 'cambio de estado'
Add-Api 1790 740 200 80 'Email API' 'envía correo'
Add-Actor 2090 720 'Empresa cliente'
Add-Terminal 2310 750 240 60 'EMPRESA VALIDADA' $OK

Add-ControlService 230 900 180 80 'SecurityService' 'rol y autorización'
Add-Database 480 900 200 80 'Auth DB' 'READ usuario · rol'
Add-Api 700 900 180 80 'SUNAT API' 'activo · habido'
Add-Api 940 900 200 80 'Credit API' 'historial crediticio'
Add-Database 1220 900 260 88 'Leasing DB · company' 'PENDING → VALIDATED'
Add-Outcome 1020 1020 190 80 "RejectionNotification`nService"

Add-CallLabel 300 835 'AUTH' $PURPLE 80
Add-CallLabel 420 912 'READ' $TEAL 70
Add-CallLabel 690 845 'WRITE company PENDING' $TEAL 220
Add-CallLabel 730 865 'CALL' $ORANGE 150
Add-CallLabel 930 865 'CALL' $ORANGE 150
Add-CallLabel 1185 750 'SÍ' $OK 60
Add-CallLabel 1080 930 'NO' $RED 60
Add-CallLabel 1270 845 'UPDATE VALIDATED' $TEAL 180
Add-CallLabel 1450 1035 'SEND rechazo al mismo Email API' $RED 250
Add-CallLabel 2550 720 'RESULTADO: perfil persistido y trazable' $OK 280

# ---------------------------------------------------------------------------
# ITERACIÓN 3 · SOLICITUD Y PREAPROBACIÓN
# ---------------------------------------------------------------------------
Add-Actor 70 1320 'Empresa cliente'
Add-Service 230 1330 200 80 'LeaseRequestService' 'crea solicitud'
Add-Service 470 1330 200 80 'AvailabilityService' 'consulta productos'
Add-Decision 700 1315 160 110 "¿Hay`ndisponibilidad?"
Add-ControlService 900 1330 200 80 'FinancialCapacityService' 'valida presupuesto'
Add-Decision 1130 1315 160 110 "¿Hay capacidad`nfinanciera?"
Add-ControlService 1330 1330 200 80 'ProviderRankingService' 'ordena candidatos'
Add-Service 1570 1330 200 80 'PreliminaryContractService' 'genera propuesta'
Add-Service 1810 1330 200 80 'NotificationService' 'envía preaprobación'
Add-Api 2050 1330 200 80 'Email API' 'contrato preliminar'
Add-Actor 2320 1320 'Empresa cliente'
Add-Terminal 2500 1340 240 60 'PREAPROBADA' $OK

Add-Database 220 1510 220 82 'Leasing DB · request' 'WRITE solicitud CREATED'
Add-Api 470 1510 200 82 'Provider API' 'READ disponibilidad'
Add-Database 880 1510 240 82 'Leasing DB · evaluation' 'READ budget · WRITE result'
Add-Database 1300 1510 240 82 'Leasing DB · ranking' 'WRITE candidatos ordenados'
Add-Database 1570 1510 200 82 'Document Store' 'WRITE contrato preliminar'
Add-Outcome 690 1640 180 75 "NO PREAPROBAR`nsin disponibilidad"
Add-Outcome 1120 1640 180 75 "NO PREAPROBAR`nsin capacidad"

Add-CallLabel 270 1450 'WRITE antes de continuar' $TEAL 180
Add-CallLabel 500 1450 'CALL' $ORANGE 140
Add-CallLabel 805 1345 'SÍ' $OK 50
Add-CallLabel 970 1450 'READ / WRITE' $TEAL 140
Add-CallLabel 1235 1345 'SÍ' $OK 50
Add-CallLabel 1370 1450 'WRITE ranking' $TEAL 150
Add-CallLabel 1600 1450 'WRITE PDF' $TEAL 140
Add-CallLabel 1900 1305 'SEND after commit' $ORANGE 150
Add-CallLabel 790 1510 'NO' $RED 50
Add-CallLabel 1220 1510 'NO' $RED 50

# ---------------------------------------------------------------------------
# ITERACIÓN 4 · APROBACIONES, CONTRATO, ORDEN Y ENTREGA
# ---------------------------------------------------------------------------
Add-Actor 325 1825 'Gerente de Ventas'
Add-Actor 555 1825 'Gerente de Logística'
Add-Actor 785 1825 'Gerente de Finanzas'
Add-Actor 1485 1825 'Empresa cliente'
Add-Actor 1950 1825 'Proveedor'
Add-Actor 2425 1825 'Empresa cliente'

Add-Terminal 60 1990 170 60 'PREAPROBADA' $OK
Add-Decision 280 1965 170 110 "SalesApprovalService`n¿aprueba?"
Add-Decision 510 1965 170 110 "LogisticsApprovalService`n¿proveedor y plazo?"
Add-Decision 740 1965 170 110 "FinanceApprovalService`n¿cuotas y cobro?"
Add-Service 970 1980 190 80 'CaseFileService' 'consolida expediente'
Add-Service 1210 1980 180 80 'ContractService' 'contrato definitivo'
Add-Decision 1440 1965 170 110 "ContractAcceptanceService`n¿cliente acepta?"
Add-Service 1670 1980 190 80 'PurchaseOrderService' 'activa orden'
Add-Service 1910 1980 180 80 'SupplierGateway' 'envía orden y recibe fecha'
Add-Service 2150 1980 180 80 'DeliveryService' 'acta de entrega'
Add-Decision 2380 1965 170 110 "ConformityService`n¿conforme ≤ 48 h?"
Add-Terminal 2610 1990 200 60 "FIN`nORDEN CONFORME" $OK

Add-Outcome 290 2140 150 65 "STOP`nno aprobada"
Add-Outcome 520 2140 150 65 "STOP`nno aprobada"
Add-Outcome 750 2140 150 65 "STOP`nno aprobada"
Add-Outcome 1435 2140 180 65 "FIN`ncontrato rechazado"
Add-Outcome 2350 2140 230 65 'IncidentService · abrir caso'

Add-Database 280 2280 170 75 'Leasing DB' 'WRITE sales approval'
Add-Database 510 2280 170 75 'Leasing DB' 'WRITE logistics approval'
Add-Database 740 2280 170 75 'Leasing DB' 'WRITE finance approval'
Add-Database 950 2280 230 82 'Leasing DB · case' 'READ 3 approvals · WRITE file'
Add-Database 1210 2280 180 82 'Document Store' 'WRITE contrato'
Add-Database 1430 2280 190 82 'Leasing DB' 'UPDATE ACCEPTED'
Add-Api 1860 2280 240 82 'Provider API' 'ORDER · delivery date'
Add-Database 2140 2280 210 82 'Leasing DB · delivery' 'WRITE acta · UPDATE conformity'

Add-ControlService 430 2430 210 80 'StateTransitionService' 'recibe cada WRITE/UPDATE'
Add-ControlService 690 2430 180 80 'AuditService' 'agrega actor y before/after'
Add-Database 920 2430 220 80 'Leasing DB · audit' 'misma transacción'
Add-Terminal 1180 2440 160 60 'COMMIT OK' $OK
Add-Service 1390 2430 220 80 'NotificationService' 'solo después del commit'
Add-Api 1660 2430 180 80 'Email API' 'SEND estado'
Add-Actor 1920 2415 'Empresa cliente'

Add-CallLabel 455 1990 'SÍ' $OK 50
Add-CallLabel 685 1990 'SÍ' $OK 50
Add-CallLabel 915 1990 'SÍ' $OK 50
Add-CallLabel 1615 1990 'SÍ' $OK 50
Add-CallLabel 2555 1990 'SÍ' $OK 50
Add-CallLabel 370 2090 'NO' $RED 50
Add-CallLabel 600 2090 'NO' $RED 50
Add-CallLabel 830 2090 'NO' $RED 50
Add-CallLabel 1530 2090 'NO' $RED 50
Add-CallLabel 2470 2090 'NO' $RED 50
Add-CallLabel 220 2240 'WRITE decisión' $TEAL 170
Add-CallLabel 450 2240 'WRITE decisión' $TEAL 170
Add-CallLabel 680 2240 'WRITE decisión' $TEAL 170
Add-CallLabel 980 2190 'READ + WRITE expediente' $TEAL 190
Add-CallLabel 1215 2190 'WRITE PDF' $TEAL 160
Add-CallLabel 1435 2190 'UPDATE ACCEPTED' $TEAL 170
Add-CallLabel 1790 2220 'CALL / RECEIVE' $ORANGE 180
Add-CallLabel 2135 2190 'WRITE acta' $TEAL 150
Add-CallLabel 2310 2220 'UPDATE CONFORME' $TEAL 180
Add-CallLabel 470 2370 'todos los servicios con WRITE/UPDATE' $TEAL 300
Add-CallLabel 870 2395 'auditoría dentro de la transacción' $TEAL 310
Add-CallLabel 1340 2395 'after commit' $RED 200

# ---------------------------------------------------------------------------
# ITERACIÓN 5 · TODOS LOS SERVICIOS E2E, TODAVÍA SIN ESCALAR
# ---------------------------------------------------------------------------
# Entrada
Add-Actor 70 2780 'Empresa cliente'
Add-Service 220 2800 180 80 'Lea$e Web' 'canal por rol'
Add-ControlService 450 2800 200 80 'API / Controllers' 'valida y enruta'
Add-ControlService 700 2800 220 80 'Lea$e App' 'monolito modular · 1 instancia'
Add-CallLabel 180 2765 'INICIO · HTTPS' $BLUE 190

# A · Acceso, registro y validación de la empresa
Add-Text 70 3020 'A · ACCESO Y EMPRESA' 12 $BLUE 'left' 240 3
Add-Service 120 3000 160 80 'LoginService' 'autentica'
Add-ControlService 310 3000 170 80 'SecurityService' 'rol y permisos'
Add-Service 510 3000 190 80 'RegisterCompanyService' 'WRITE PENDING'
Add-ControlService 730 3000 200 80 'CompanyValidationService' 'SUNAT + crédito'
Add-Decision 960 2985 150 110 "¿empresa`nválida?"
Add-Service 1150 3000 200 80 'CompanyProfileService' 'UPDATE VALIDATED'
Add-Terminal 1390 3010 200 60 'EMPRESA VALIDADA' $OK
Add-Outcome 935 3120 200 60 'REGISTRO RECHAZADO'
Add-CallLabel 1070 2960 'SÍ' $OK 60
Add-CallLabel 1050 3110 'NO' $RED 60

# B · Solicitud y preaprobación
Add-Text 70 3230 'B · SOLICITUD Y PREAPROBACIÓN' 12 $BLUE 'left' 310 3
Add-Service 120 3210 170 80 'LeaseRequestService' 'WRITE CREATED'
Add-Service 320 3210 180 80 'AvailabilityService' 'consulta productos'
Add-Decision 530 3195 150 110 "¿hay`nstock?"
Add-ControlService 710 3210 190 80 'FinancialCapacityService' 'evalúa presupuesto'
Add-Decision 930 3195 150 110 "¿hay`ncapacidad?"
Add-ControlService 1110 3210 190 80 'ProviderRankingService' 'ordena candidatos'
Add-Service 1330 3210 210 80 'PreliminaryContractService' 'genera propuesta'
Add-Terminal 1580 3220 180 60 'PREAPROBADA' $OK
Add-Outcome 525 3330 160 60 'SIN STOCK'
Add-Outcome 915 3330 180 60 'CAPACIDAD INSUFICIENTE'
Add-CallLabel 640 3170 'SÍ' $OK 60
Add-CallLabel 1040 3170 'SÍ' $OK 60
Add-CallLabel 610 3305 'NO' $RED 60
Add-CallLabel 1010 3305 'NO' $RED 60

# C · Aprobaciones y contratación; los actores están sobre su decisión
Add-Text 70 3555 'C · APROBACIONES Y CONTRATO' 12 $BLUE 'left' 310 3
Add-Actor 270 3420 'Gerente de Ventas'
Add-Actor 480 3420 'Gerente de Logística'
Add-Actor 700 3420 'Gerente de Finanzas'
Add-Actor 1365 3420 'Empresa cliente'
Add-Terminal 50 3550 150 60 'PREAPROBADA' $OK
Add-Decision 230 3535 160 110 'SalesApprovalService'
Add-Decision 430 3535 180 110 'LogisticsApprovalService'
Add-Decision 650 3535 180 110 'FinanceApprovalService'
Add-Service 870 3540 180 80 'CaseFileService' 'consolida expediente'
Add-Service 1090 3540 180 80 'ContractService' 'contrato definitivo'
Add-Decision 1310 3535 190 110 'ContractAcceptanceService'
Add-Service 1540 3540 200 80 'ContractRepository' 'UPDATE ACCEPTED'
Add-Terminal 1780 3550 190 60 'CONTRATO ACEPTADO' $OK
Add-Outcome 230 3670 160 60 'VENTAS: NO'
Add-Outcome 430 3670 180 60 'LOGÍSTICA: NO'
Add-Outcome 650 3670 180 60 'FINANZAS: NO'
Add-Outcome 1310 3670 190 60 'CONTRATO RECHAZADO'
Add-CallLabel 385 3510 'SÍ' $OK 50
Add-CallLabel 605 3510 'SÍ' $OK 50
Add-CallLabel 825 3510 'SÍ' $OK 50
Add-CallLabel 1500 3510 'SÍ' $OK 50
Add-CallLabel 320 3645 'NO' $RED 50
Add-CallLabel 530 3645 'NO' $RED 50
Add-CallLabel 750 3645 'NO' $RED 50
Add-CallLabel 1415 3645 'NO' $RED 50

# D · Orden, entrega y cierre
Add-Text 70 3910 'D · ORDEN Y ENTREGA' 12 $BLUE 'left' 260 3
Add-Actor 390 3760 'Proveedor'
Add-Actor 850 3760 'Empresa cliente'
Add-Service 120 3890 190 80 'PurchaseOrderService' 'activa orden'
Add-Service 350 3890 190 80 'SupplierGateway' 'orden + fecha'
Add-Service 580 3890 190 80 'DeliveryService' 'WRITE acta'
Add-Decision 810 3875 180 110 "ConformityService`n¿conforme ≤ 48 h?"
Add-Terminal 1030 3900 200 60 "FIN`nORDEN CONFORME" $OK
Add-Outcome 810 4020 180 60 'IncidentService · NO conforme'
Add-CallLabel 990 3850 'SÍ' $OK 50
Add-CallLabel 930 3995 'NO' $RED 50

# Flujo transversal real: guardar estado y auditoría, confirmar y recién notificar
Add-Text 70 4150 'PERSISTENCIA, AUDITORÍA Y NOTIFICACIÓN DE CADA CAMBIO DE ESTADO' 12 $PURPLE 'left' 620 3
Add-ControlService 100 4170 180 80 'StateTransitionService' 'recibe WRITE / UPDATE'
Add-ControlService 330 4170 190 80 'AuditService' 'actor · before/after · time'
Add-Database 570 4170 280 80 'Leasing DB' 'estado + auditoría · misma transacción'
Add-Terminal 900 4180 160 60 'COMMIT OK' $OK
Add-Service 1110 4170 220 80 'NotificationService' 'solo después del commit'
Add-Api 1370 4170 190 80 'Email API' 'SEND estado'
Add-Actor 1610 4155 'Empresa cliente'
Add-Database 1940 4170 260 80 'Document Store' 'contratos · acta'
Add-Api 2280 2980 300 100 'External APIs' 'SUNAT · Credit · Provider'
Add-CallLabel 505 4145 'misma transacción' $PURPLE 180
Add-CallLabel 1010 4145 'after commit' $RED 160
Add-CallLabel 1500 4145 'una sola Email API' $ORANGE 180

# Nota final: la confiabilidad se dibuja aparte para no mezclar responsabilidades
Add-Rect 70 4330 2720 150 $GRAY 'transparent' -Dashed -Rough 0 -StrokeWidth 1
Add-Text 90 4345 'CÓMO LEER LA ITERACIÓN FINAL' 13 $INK 'left' 420
Add-Text 90 4375 'Siga las flechas verdes A → B → C → D: el flujo inicia en Empresa cliente y termina en ORDEN CONFORME o en una salida NO explícita.' 11 $BODY 'left' 1330
Add-Text 90 4405 'Cada WRITE/UPDATE baja al mismo flujo transversal: estado + auditoría → COMMIT OK → NotificationService → una única Email API.' 11 $BODY 'left' 1330
Add-Text 1490 4345 'LÍNEA BASE SIN ESCALAR' 13 $ORANGE 'left' 350
Add-Text 1490 4375 'Una instancia de Lea$e App, una Leasing DB lógica y llamadas directas a dependencias externas.' 11 $BODY 'left' 1180
Add-Text 1490 4405 'Load balancing, health endpoints, réplicas y patrones de reliability aparecen en el diagrama separado.' 11 $BODY 'left' 1180

$document = [ordered]@{
    type = 'excalidraw'
    version = 2
    source = 'https://excalidraw.com'
    elements = @($elements)
    appState = @{ gridSize = $null; viewBackgroundColor = '#ffffff' }
    files = @{}
}

$generatorRoot = if ([string]::IsNullOrWhiteSpace($PSScriptRoot)) {
    $env:LAB6_DIAGRAM_GENERATOR_ROOT
} else {
    $PSScriptRoot
}
$output = Join-Path (Split-Path $generatorRoot -Parent) 'diagrama-top-down.excalidraw'
$json = $document | ConvertTo-Json -Depth 20
[System.IO.File]::WriteAllText($output, $json, [System.Text.UTF8Encoding]::new($false))
Write-Output "$output ($($elements.Count) elementos)"

# ===========================================================================
# DIAGRAMA SEPARADO · ESCALAMIENTO CON CONFIABILIDAD
# Parte del E2E consolidado y agrega mecanismos operativos sin mezclarlos con
# las iteraciones de descubrimiento top-down.
# ===========================================================================
$elements.Clear()

Add-Zone 40 165 2820 430 '1 · ENTRADA REDUNDANTE Y HEALTH ENDPOINTS' 'Todos los roles entran por el balanceador; solo las réplicas READY reciben tráfico.'
Add-Zone 40 625 2820 480 '2 · MISMO HAPPY PATH E2E EN CADA RÉPLICA' 'Las instancias ejecutan los mismos módulos A → B → C → D; escalar no cambia la secuencia de negocio.'
Add-Zone 40 1135 2820 475 '3 · AISLAMIENTO Y PROTECCIÓN DE DEPENDENCIAS' 'Tres bulkheads evitan que una dependencia caída agote los recursos de las demás.'
Add-Zone 40 1640 2820 390 '4 · DATOS, FAILOVER Y ENTREGA ASÍNCRONA' 'Estado, auditoría y outbox se confirman juntos; broker y workers desacoplan el correo.'
Add-Zone 40 2060 2820 310 '5 · DEGRADACIÓN ELEGANTE, OBSERVABILIDAD Y CHAOS' 'El sistema conserva un estado honesto, alerta y prueba periódicamente sus mecanismos de recuperación.'

# ---------------------------------------------------------------------------
# Conectores · se agregan antes para dejarlos detrás de los nodos
# ---------------------------------------------------------------------------
# Roles → Load Balancer → réplicas
Add-Arrow '150,340;880,340' $BLUE
Add-Arrow '370,340;880,340' $BLUE
Add-Arrow '590,340;880,340' $BLUE
Add-Arrow '810,340;880,340' $BLUE
Add-Arrow '1080,340;1160,290' $OK
Add-Arrow '1080,340;1470,290' $OK
Add-Arrow '1080,340;1780,290' $OK
# Health checks y observabilidad
Add-Arrow '1270,360;1270,420;2190,420;2190,350' $PURPLE -Dashed
Add-Arrow '1580,360;1580,430;2190,430;2190,350' $PURPLE -Dashed
Add-Arrow '1890,360;1890,440;2190,440;2190,350' $PURPLE -Dashed
Add-Arrow '2320,290;2400,290' $PURPLE
Add-Arrow '2490,350;2490,390;980,390;980,380' $RED -Dashed
Add-Arrow '1270,360;1270,480;2190,480' $TEAL -Dashed
Add-Arrow '1580,360;1580,490;2190,490' $TEAL -Dashed
Add-Arrow '1890,360;1890,500;2190,500' $TEAL -Dashed

# Secuencia E2E
Add-Arrow '620,850;740,850' $OK
Add-Arrow '1260,850;1380,850' $OK
Add-Arrow '1900,850;2020,850' $OK
Add-Arrow '2540,850;2630,850' $OK

# E2E → bulkheads correspondientes
Add-Arrow '360,930;360,1200;250,1200' $ORANGE -Dashed
Add-Arrow '1000,930;1000,1330;250,1330' $ORANGE -Dashed
Add-Arrow '2280,930;2280,1460;250,1460' $ORANGE -Dashed

# Tres carriles aislados
Add-Arrow '350,1230;410,1230' $ORANGE
Add-Arrow '670,1230;720,1230' $ORANGE
Add-Arrow '940,1230;1000,1230' $ORANGE
Add-Arrow '350,1360;410,1360' $ORANGE
Add-Arrow '670,1360;720,1360' $ORANGE
Add-Arrow '940,1360;1000,1360' $ORANGE
Add-Arrow '350,1490;410,1490' $ORANGE
Add-Arrow '670,1490;720,1490' $ORANGE
Add-Arrow '940,1490;1000,1490' $ORANGE

# Estado de circuitos y recursos separados
Add-Arrow '1260,1230;1320,1230' $RED -Dashed
Add-Arrow '1260,1360;1320,1360' $RED -Dashed
Add-Arrow '1260,1490;1320,1490' $RED -Dashed

# Datos: réplica, failover, backup
Add-Arrow '390,1735;450,1735' $TEAL
Add-Arrow '390,1765;730,1765' $TEAL
Add-Arrow '390,1795;1010,1795' $TEAL
# Transacción → outbox → broker → workers → idempotencia
Add-Arrow '1440,1745;1490,1745' $PURPLE
Add-Arrow '1700,1745;1750,1745' $PURPLE
Add-Arrow '1970,1745;2020,1745' $PURPLE
Add-Arrow '2240,1745;2290,1745' $PURPLE
Add-Arrow '2500,1745;2600,1745;2600,1490;1260,1490' $ORANGE
# Documentos y trazas
Add-Arrow '290,1930;450,1930' $TEAL
Add-Arrow '700,1930;760,1930' $TEAL
Add-Arrow '1010,1930;1070,1930' $TEAL

# Chaos inyecta fallas controladas; observabilidad verifica recuperación
Add-Arrow '2020,2185;2110,2185' $RED -Dashed
Add-Arrow '2440,2185;2500,2185' $TEAL
Add-Arrow '1780,2140;1780,520;2320,520' $RED -Dashed
Add-Arrow '1780,2225;1780,2000;560,2000;560,1790' $RED -Dashed
Add-Arrow '1780,2260;1780,2015;1860,2015;1860,1785' $RED -Dashed

# ---------------------------------------------------------------------------
# Cabecera y leyenda
# ---------------------------------------------------------------------------
Add-Text 55 35 'LEA$E · ARQUITECTURA ESCALADA CON RELIABILITY' 28 $BLUE 'left' 1000 3
Add-Text 55 78 'Parte de la Iteración 5 completa y agrega tolerancia a fallas, recuperación y evidencia operativa.' 14 $GRAY 'left' 1200
Add-Text 55 112 'Las réplicas conservan el monolito modular; los patrones se aplican en los bordes, datos y trabajos asíncronos.' 11 $BODY 'left' 1250
Add-Box 1850 45 180 55 $BLUE $BLUE_FILL 'Servicio / réplica' '' 10
Add-Box 2050 45 180 55 $PURPLE $PURPLE_FILL 'Reliability' '' 10
Add-Box 2250 45 180 55 $ORANGE $YELLOW_FILL 'Dependencia' '' 10 -Dashed
Add-Database 2450 43 180 58 'Datos' 'replicados'
Add-Terminal 2650 45 160 55 'ESTADO' $OK

# ---------------------------------------------------------------------------
# 1 · Entrada redundante
# ---------------------------------------------------------------------------
Add-Actor 70 235 'Empresa cliente'
Add-Actor 290 235 'Gerente de Ventas'
Add-Actor 510 235 'Gerente de Logística'
Add-Actor 730 235 'Gerente de Finanzas'
Add-ControlService 880 300 200 80 'Load Balancer' 'routing · elimina unhealthy'
Add-ControlService 1160 220 220 140 'App Instance 1' 'READY · módulos A–D'
Add-ControlService 1470 220 220 140 'App Instance 2' 'READY · módulos A–D'
Add-ControlService 1780 220 220 140 'App Instance N+1' 'READY / reemplazo'
Add-ControlService 2080 250 240 100 'Health Endpoints' '/health/live · /health/ready'
Add-ControlService 2400 250 210 100 'Orchestrator' 'restart · reschedule'
Add-ControlService 2080 450 240 80 'Observability Agent' 'metrics · logs · traces'
Add-ControlService 2400 450 210 80 'Autoscaling' 'CPU · latency · queue'
Add-CallLabel 880 250 'HTTPS autenticado' $BLUE 200
Add-CallLabel 2080 210 'cada réplica publica salud' $PURPLE 260
Add-CallLabel 2380 370 'NO READY → fuera del pool' $RED 250

# ---------------------------------------------------------------------------
# 2 · Happy path E2E completo dentro de cada réplica
# ---------------------------------------------------------------------------
Add-Box 100 700 520 300 $BLUE $BLUE_FILL 'A · Acceso y empresa' "LoginService → SecurityService`nRegisterCompanyService`nCompanyValidationService → decisión`nCompanyProfileService`nFIN: EMPRESA VALIDADA / RECHAZADA" 13
Add-Box 740 700 520 300 $BLUE $BLUE_FILL 'B · Solicitud y preaprobación' "LeaseRequestService`nAvailabilityService → decisión`nFinancialCapacityService → decisión`nProviderRankingService`nPreliminaryContractService`nFIN: PREAPROBADA / NO PREAPROBADA" 13
Add-Box 1380 700 520 300 $BLUE $BLUE_FILL 'C · Aprobaciones y contrato' "SalesApprovalService`nLogisticsApprovalService`nFinanceApprovalService`nCaseFileService → ContractService`nContractAcceptanceService`nContractRepository`nFIN: CONTRATO ACEPTADO / RECHAZADO" 13
Add-Box 2020 700 520 300 $BLUE $BLUE_FILL 'D · Orden y entrega' "PurchaseOrderService`nSupplierGateway`nDeliveryService`nConformityService → decisión`nIncidentService si NO`nFIN: ORDEN CONFORME" 13
Add-Terminal 2630 820 150 60 'FIN E2E' $OK
Add-Text 100 1020 'Cada cambio pasa por StateTransitionService + AuditService; el COMMIT ocurre antes de publicar la notificación.' 11 $PURPLE 'left' 1450
Add-Text 1600 1020 'Roles: cliente en A/B/C/D · gerentes en C · proveedor en B/D.' 11 $BODY 'left' 1100

# ---------------------------------------------------------------------------
# 3 · Bulkheads, retries y circuit breakers
# ---------------------------------------------------------------------------
Add-ControlService 90 1190 260 80 'Bulkhead · Validaciones' 'pool/conexiones aisladas'
Add-ControlService 410 1190 260 80 'Retry + Exp. Backoff' 'máx. 3 · jitter · solo seguro'
Add-ControlService 720 1190 220 80 'Circuit Breaker #1' 'CLOSED · OPEN · HALF-OPEN'
Add-Api 1000 1190 260 80 'SUNAT + Credit APIs' 'timeout estricto'

Add-ControlService 90 1320 260 80 'Bulkhead · Proveedor' 'pool/conexiones aisladas'
Add-ControlService 410 1320 260 80 'Retry + Exp. Backoff' 'idempotency key · acotado'
Add-ControlService 720 1320 220 80 'Circuit Breaker #2' 'CLOSED · OPEN · HALF-OPEN'
Add-Api 1000 1320 260 80 'Provider API' 'stock · orden · fecha'

Add-ControlService 90 1450 260 80 'Bulkhead · Notificación' 'workers/conexiones aisladas'
Add-ControlService 410 1450 260 80 'Retry + Exp. Backoff' 'máx. intentos · DLQ'
Add-ControlService 720 1450 220 80 'Circuit Breaker #3' 'CLOSED · OPEN · HALF-OPEN'
Add-Api 1000 1450 260 80 'Email API' 'correo externo'

Add-ControlService 1320 1190 310 80 'Timeout Budget' 'validaciones rápidas < 3 s'
Add-ControlService 1320 1320 310 80 'IdempotencyService' 'request-id · evita doble orden'
Add-ControlService 1320 1450 310 80 'Dead Letter Queue' 'mensaje agotó reintentos'
Add-Box 1710 1190 1050 340 $PURPLE $PURPLE_FILL 'AISLAMIENTO DE FALLAS' "• Cada bulkhead tiene su propio pool de hilos y conexiones.`n• La caída de Email API no consume recursos de SUNAT ni del proveedor.`n• Retries: solo errores transitorios y operaciones seguras/idempotentes.`n• Backoff exponencial + jitter evita tormentas de reintentos.`n• Circuit breaker falla rápido mientras la dependencia se recupera.`n• Timeout total de la validación respeta el SLO menor a 3 segundos." 14

# ---------------------------------------------------------------------------
# 4 · Datos y mensajería confiable
# ---------------------------------------------------------------------------
Add-Database 100 1700 290 100 'Leasing DB Primary' 'estado · audit · outbox · ACID'
Add-Database 450 1700 220 80 'Standby' 'failover automático'
Add-Database 730 1700 220 80 'Read Replica' 'lecturas · dashboards'
Add-Database 1010 1700 220 80 'Backups + PITR' 'restore probado'

Add-ControlService 1250 1700 190 90 'TransactionService' 'estado + audit + outbox'
Add-Database 1490 1700 210 90 'Outbox Table' 'mismo COMMIT'
Add-ControlService 1750 1700 220 90 'Broker Cluster' 'cola durable · réplica'
Add-ControlService 2020 1700 220 90 'Workers N+1' 'ack después de enviar'
Add-ControlService 2290 1700 210 90 'Idempotency' 'deduplica evento'

Add-Database 100 1890 190 80 'Document Store' 'contrato · acta'
Add-Database 450 1890 250 80 'Replica + Versioning' 'recupera documento'
Add-Database 760 1890 250 80 'Audit Log' 'append-only · retención'
Add-Database 1070 1890 250 80 'Telemetry Store' 'metrics · logs · traces'
Add-Text 1390 1895 'EMAIL CAÍDO: el COMMIT sigue válido; el evento permanece en outbox/broker y se reintenta sin duplicar.' 12 $OK 'left' 1300 3
Add-Text 1390 1940 'DB PRIMARY CAÍDA: se promueve Standby; readiness retira temporalmente instancias sin conexión.' 12 $TEAL 'left' 1300

# ---------------------------------------------------------------------------
# 5 · Degradación elegante, chaos y alertas
# ---------------------------------------------------------------------------
Add-Box 70 2110 1280 210 $OK $OK_FILL 'DEGRADACIÓN ELEGANTE' "• SUNAT/Credit no disponible → REGISTRO PENDIENTE; nunca rechazo falso.`n• Provider API no disponible → SOLICITUD PENDIENTE; no activar orden.`n• Email API no disponible → estado confirmado + notificación pendiente.`n• Lectura no crítica caída → mostrar último estado con advertencia.`n• Document Store caído → conservar expediente; generar documento al recuperarse." 14
Add-Box 1470 2110 550 210 $RED $RED_FILL 'CHAOS ENGINEERING' "Experimentos controlados:`n• detener una App Instance`n• abrir un circuit breaker`n• pausar un nodo del broker`n• forzar failover del DB Primary`nVerificar SLO, alertas y recuperación." 14 -Dashed
Add-ControlService 2110 2110 330 160 'ObservabilityService' 'latencia · error rate · saturation`nqueue lag · breaker state · failover'
Add-ControlService 2500 2110 250 160 'Alerting + Runbooks' 'SLO breach → on-call`nacciones de recuperación'
Add-Text 2110 2290 'Chaos se ejecuta en ambientes controlados y con abort conditions.' 10 $RED 'left' 650

$reliabilityDocument = [ordered]@{
    type = 'excalidraw'
    version = 2
    source = 'https://excalidraw.com'
    elements = @($elements)
    appState = @{ gridSize = $null; viewBackgroundColor = '#ffffff' }
    files = @{}
}

$reliabilityOutput = Join-Path (Split-Path $generatorRoot -Parent) 'diagrama-reliability.excalidraw'
$reliabilityJson = $reliabilityDocument | ConvertTo-Json -Depth 20
[System.IO.File]::WriteAllText($reliabilityOutput, $reliabilityJson, [System.Text.UTF8Encoding]::new($false))
Write-Output "$reliabilityOutput ($($elements.Count) elementos)"
