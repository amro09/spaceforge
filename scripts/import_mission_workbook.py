"""Repeatable XLSX -> JSON + browser data. No guessed values; blank cells stay null."""
import argparse
import hashlib
import json
from pathlib import Path
import openpyxl

parser = argparse.ArgumentParser()
parser.add_argument("workbook", nargs="?", default="attached_assets/Mission_Forge_Data_Pack_1794689600166.xlsx")
args = parser.parse_args()
source = Path(args.workbook)
wb = openpyxl.load_workbook(source, read_only=True, data_only=True)
sheets = {s.title: [list(row) for row in s.values] for s in wb}
def records(name, start=4):
    rows=sheets[name]
    return [(i+1,row) for i,row in enumerate(rows) if i+1>=start and row[0] is not None]

sources=[{"title":r[0],"url":r[1],"confidence":r[2]} for _,r in records("7_Sources",3)]
rockets=[]
for (row,r),key in zip(records("2_Launch_Vehicles"),["electron","falcon9","falconHeavy","vulcan","newGlenn","atlasV"]):
    rockets.append({"id":key,"name":r[0],"class":r[1],"capacity":{"LEO":r[2],"GTO":r[3],"TLI":r[4],"MARS":r[5]},
                    "priceLow":r[6],"priceHigh":r[7],"notes":r[8],"confidence":r[9],"source":r[10],"row":row})
instruments=[]
for sheet,mission,ids in [
    ("3_Moon_Instruments","moon",["lroc","lola","diviner","lamp","lend","crater","minirf"]),
    ("4_Mars_Instruments","mars",["hirise","ctx","marci","crism","mcs","sharad"])]:
    for (row,r),key in zip(records(sheet),ids):
        instruments.append({"id":key,"mission":mission,"name":r[0],"type":r[1],"mass":r[2],"power":r[3],
                            "description":r[4],"goal":r[5],"confidence":r[6],"source":r[7],"cost":None,"sheet":sheet,"row":row})
data={"workbook":source.name,"sha256":hashlib.sha256(source.read_bytes()).hexdigest(),
      "units":{"mass":"kg","capacity":"kg","power":"W","price":"million USD","deltaV":"km/s"},
      "sheets":sheets,"rockets":rockets,"instruments":instruments,"sources":sources,
      "levels":[{"name":r[0],"body":r[1],"goal":r[2],"instruments":r[3],"orbit":r[4],"budget":r[5],"notes":r[6],"confidence":r[7]} for _,r in records("6_Proposed_Levels") if isinstance(r[5],(int,float))]}
assert data["instruments"][0]["mass"]+data["instruments"][1]["mass"] == 30.5
assert round(data["instruments"][0]["power"]+data["instruments"][1]["power"],1)==57.4
assert next(i for i in instruments if i["id"]=="sharad")["power"] is None
out=Path("artifacts/mission-forge/public/data")
out.mkdir(parents=True,exist_ok=True)
payload=json.dumps(data,ensure_ascii=False,indent=2,allow_nan=False)
(out/"mission-workbook.json").write_text(payload)
(out/"mission-workbook.js").write_text("window.MISSION_WORKBOOK = "+payload+";\n")
print(f"Imported {len(sheets)} sheets, {len(rockets)} rockets, {len(instruments)} instruments. Blank cells preserved.")
