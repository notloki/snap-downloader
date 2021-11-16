$snap_name = $args[0]
 
if($args[1] -eq $null) {
      $arch = 'arm64'
} else {
      $arch = $args[1]
}
 
$snap_api_uri = 'http://api.snapcraft.io/v2/snaps/info/' + $snap_name
$outfile_name = $snap_name + '_' + $arch + '.snap'
 
try{
      $snap_uri = Invoke-WebRequest $snap_api_uri -Headers @{"Accept" = "application/json";"Snap-Device-Series"="16"} | Select-Object -Expand Content
  $vPSObject = $snap_uri | ConvertFrom-Json
 
  $found = 0;
  foreach($vers in $vPSObject[0]."channel-map") {
        if ($vers.channel.risk -eq 'stable'){
          if ($vers.channel.architecture -eq $arch){
                $found=1;
                Invoke-WebRequest -Uri $vers.download.url -OutFile $outfile_name
      }
    }
  }
 
  if($found -eq 0) {
        Write-host 'No' $arch 'snap available' -fore red
  } else {
        Write-host 'Download succeeded' -fore green
  }
} catch {
      Write-host 'An error occured. Download interrupted. Error Description:' -fore red
  Write-host $_ -fore red
}