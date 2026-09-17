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
# Servicios transversales
Add-Arrow '970,2470;1160,2470' $TEAL
Add-Arrow '1430,2470;1660,2470' $RED
Add-Arrow '1840,2470;2050,2470' $ORANGE

# ---------------------------------------------------------------------------
# CABECERA Y LEYENDA
# ---------------------------------------------------------------------------
Add-Text 55 35 'TOP DOWN DESIGN · LEA$E' 28 $BLUE 'left' 700 3
Add-Text 55 78 'Parte 1 · arquitectura básica sin escalar · del contexto a los servicios y datos' 14 $GRAY 'left' 900
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

Add-ControlService 970 2430 190 80 'AuditService' 'cada decisión y transición'
Add-Database 1160 2430 230 80 'Audit DB' 'actor · before/after · time'
Add-Service 1430 2430 230 80 'NotificationService' 'después del commit'
Add-Api 1660 2430 180 80 'Email API' 'SEND estado'
Add-Actor 2050 2415 'Empresa cliente'

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
Add-CallLabel 970 2395 'toda transición' $TEAL 190
Add-CallLabel 1430 2395 'after commit' $RED 200

# Nota de modelado y límite de Parte 1
Add-Rect 40 2680 2820 130 $GRAY 'transparent' -Dashed -Rough 0 -StrokeWidth 1
Add-Text 60 2695 'CÓMO LEER LOS DATOS' 13 $INK 'left' 250
Add-Text 60 2722 'Los nodos “Leasing DB · company/request/approval/delivery” son vistas lógicas de una sola base transaccional en la Parte 1.' 11 $BODY 'left' 1350
Add-Text 60 2750 'La flecha llega a la base exactamente cuando ocurre el READ, WRITE o UPDATE; el flujo continúa después de confirmar la escritura.' 11 $BODY 'left' 1400
Add-Text 60 2780 'Si un componente reaparece en otra iteración, es el mismo componente visto con mayor detalle; no es otra instancia.' 10 $GRAY 'left' 1350
Add-Text 1550 2695 'AÚN NO ESCALADO' 13 $RED 'left' 240
Add-Text 1550 2722 '1 aplicación · 1 base · llamadas síncronas · sin réplicas, colas, reintentos, circuit breaker, balanceador ni failover.' 11 $RED 'left' 1220
Add-Text 1550 2750 'Esos elementos se incorporan en la Parte 3 (Reliability), después del consenso grupal.' 11 $GRAY 'left' 1100

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
$output = Join-Path (Split-Path $generatorRoot -Parent) 'parte1-arquitectura-basica.excalidraw'
$json = $document | ConvertTo-Json -Depth 20
[System.IO.File]::WriteAllText($output, $json, [System.Text.UTF8Encoding]::new($false))
Write-Output "$output ($($elements.Count) elementos)"
