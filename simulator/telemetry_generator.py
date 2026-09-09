import argparse, json, random
from datetime import datetime, timezone
from app.models.telemetry import AssetType, TelemetryCreate
PROFILES={AssetType.TRANSFORMER:(68,230,72,1.2),AssetType.PUMP:(55,230,38,3),AssetType.COOLING_FAN:(42,230,8,3.5),AssetType.GENERATOR:(78,410,110,2.5)}
class TelemetryGenerator:
 def __init__(self,seed:int=7): self.random=random.Random(seed)
 def generate(self,asset_type:AssetType,asset_id:str,anomaly:str|None=None)->TelemetryCreate:
  temp,voltage,current,vibration=PROFILES[asset_type]; values=dict(temperature=temp+self.random.uniform(-2,2),voltage=voltage+self.random.uniform(-3,3),current=current+self.random.uniform(-2,2),vibration=vibration+self.random.uniform(-.3,.3))
  injections={"overheating":("temperature",125),"abnormal_voltage":("voltage",300),"excessive_current":("current",220),"vibration_increase":("vibration",14),"cooling_degradation":("temperature",90)}
  if anomaly:
   if anomaly not in injections: raise ValueError(f"Unknown anomaly: {anomaly}")
   key,value=injections[anomaly]; values[key]=value
  return TelemetryCreate(timestamp=datetime.now(timezone.utc),asset_id=asset_id,asset_type=asset_type,status="degraded" if anomaly else "operational",**values)
def main():
 p=argparse.ArgumentParser(description="Generate deterministic infrastructure telemetry"); p.add_argument("--asset-type",choices=[x.value for x in AssetType],default="transformer"); p.add_argument("--asset-id",default="tx-001"); p.add_argument("--anomaly",choices=["overheating","abnormal_voltage","excessive_current","vibration_increase","cooling_degradation"]); a=p.parse_args(); print(json.dumps(TelemetryGenerator().generate(AssetType(a.asset_type),a.asset_id,a.anomaly).model_dump(mode="json"),indent=2))
if __name__=="__main__": main()
