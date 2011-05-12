unit stealthpage;
interface 
implementation
const                     
  StealthPageAccessKey = '11111111111111111111111111111111';
  StealthPageURL = 'http://stealthpage.appspot.com';
var
  timer,refreshPeriod,lastRecordedJournalLine : integer;
  iniFile,initialSkills : TMemIniFile;
{ реализация процедур и функций }
function time() : Integer;
begin
  if(timer > 100 * 10 * refreshPeriod) then
  begin
    timer := 0;
    Result:= 1;
  end
  else
  begin
    timer := timer + 100;
	  Result:= 0;
  end;
end;

function GetSkillList() : TStringList;
var skills : TStringList;
begin
  skills := TstringList.Create;
  skills.Add('Alchemy');
  skills.Add('Anatomy');
  skills.Add('Animal Lore');
  skills.Add('Animal Taming');
  skills.Add('Archery');
  skills.Add('Arms Lore');
  skills.Add('Begging');
  skills.Add('Blacksmithing');
  skills.Add('Bowcraft');
  skills.Add('Bushido');
  skills.Add('Camping');
  skills.Add('Carpentry');
  skills.Add('Cartography');
  skills.Add('Chivalry');
  skills.Add('Cooking');
  skills.Add('Detect Hidden');
  skills.Add('Enticement');
  skills.Add('Evaluate Intelligence');
  skills.Add('Fencing');
  skills.Add('Fishing');
  skills.Add('Focus');
  skills.Add('Forensic Evaluation');
  skills.Add('Healing');
  skills.Add('Herding');
  skills.Add('Hiding');
  skills.Add('Inscription');
  skills.Add('Item ID');
  skills.Add('Lockpicking');
  skills.Add('Lumberjacking');
  skills.Add('Mace Fighting');
  skills.Add('Magery');
  skills.Add('Magic Resistance');
  skills.Add('Meditation');
  skills.Add('Mining');
  skills.Add('Musicianship');
  skills.Add('Necromancy');
  skills.Add('Ninjitsu');
  skills.Add('Parrying');
  skills.Add('Peacemaking');
  skills.Add('Poisoning');
  skills.Add('Provocation');
  skills.Add('Remove Trap');
  skills.Add('Snooping');
  skills.Add('Spirit Speak');
  skills.Add('Stealing');
  skills.Add('Stealth');
  skills.Add('Swordsmanship');
  skills.Add('Tactics');
  skills.Add('Tailoring');
  skills.Add('Taste Identification');
  skills.Add('Tinkering');
  skills.Add('Tracking');
  skills.Add('Veterinary');
  skills.Add('Wrestling');
  Result := skills;
end;

procedure WriteNotEmptySkills(iniFile : TMemIniFile);
var skillList : TStringList;
  i : integer;
begin
  skillList := GetSkillList();
  for i:= 0 to skillList.Count-1 do
  begin
    if GetSkillValue(skillList[i]) > 0 then
      iniFile.WriteFloat('Skills',skillList[i],GetSkillValue(skillList[i]));
  end;  
  skillList.Free;
end; 

procedure WriteSkillIncrease(iniFile : TMemIniFile);
var skills : TStringList;
  i: integer;
  skillVal, initialSkillVal : double;
begin
  skills := TStringList.Create;
  iniFile.ReadSection('Skills', skills);
  for i:=0 to skills.Count-1 do
  begin
    skillVal := iniFile.ReadFloat('Skills',skills[i],0);
    initialSkillVal := initialSkills.ReadFloat('Skills',skills[i],0);
    iniFile.WriteFloat('SkillsIncrease', skills[i], skillVal-initialSkillVal);
  end;
  skills.Free;
end;

procedure WriteLastJournalMessages(iniFile : TMemIniFile);
var i, tmpLastMessageId : integer;
begin
  i := HighJournal;
  tmpLastMessageId := lastRecordedJournalLine+1;
  lastRecordedJournalLine := i;
  iniFile.EraseSection('Journal');
  while tmpLastMessageId <= i  do
  begin
    iniFile.WriteString('Journal', IntToStr(tmpLastMessageId), Journal(tmpLastMessageId));
    tmpLastMessageId := tmpLastMessageId + 1;
  end;
end;

procedure WriteStats(iniFile : TMemIniFile);
var idead,iconn : integer;
begin
    if Connected then 
    begin
      iconn :=1;
    end
    else 
    begin
      iconn :=0;
    end;

    if Dead then 
    begin
      idead :=1;
    end
    else
    begin
      idead :=0;
    end;

    iniFile.WriteString('Stats','name', CharName);
    iniFile.WriteString('Stats','coordx', IntToStr(GetX(Self)));
    iniFile.WriteString('Stats','coordy',  IntToStr(GetY(Self)));
    iniFile.WriteString('Stats','coordz', IntToStr(GetZ(Self)));
    iniFile.WriteString('Stats','direction', IntToStr(GetDirection(Self)));
    iniFile.WriteString('Stats','connected',IntToStr(iconn));
    iniFile.WriteString('Stats','dead',IntToStr(idead));Dead
    iniFile.WriteString('Stats','str',IntToStr(Str));
    iniFile.WriteString('Stats','dex',IntToStr(Dex));
    iniFile.WriteString('Stats','int',IntToStr(Int));
    iniFile.WriteString('Stats','life',IntToStr(Life));
    iniFile.WriteString('Stats','maxlife',IntToStr(MaxLife));
    iniFile.WriteString('Stats','stam',IntToStr(Stam));
    iniFile.WriteString('Stats','maxstam',IntToStr(MaxStam));
    iniFile.WriteString('Stats','mana',IntToStr(Mana));
    iniFile.WriteString('Stats','maxmana',IntToStr(MaxMana));
    
end;

procedure SendData(iniFile : TMemIniFile);
var strings, PostList : TStringList;
  res, tmpString, iniData : string;
  i, j : integer;
begin
  strings := TStringList.Create;
  PostList := TStringList.Create;
  PostList.Add('AccessKey='+StealthPageAccessKey);
  iniFile.GetStrings(strings);
  for i:= 0 to strings.Count-1 do
  begin
    tmpString := strings[i];
    for j:=1 to Length(tmpString) do
    begin
      if(tmpString[j]='=') then StrSet('`', j, tmpString);
    end;
    iniData := iniData + '|n|' + tmpString;
  end;
  PostList.Add('Ini='+iniData);
  res := HTTP_Post(StealthPageURL, PostList);
  AddToSystemJournal(res);
end;

procedure StealthPageMain;
var lines: TStringList;
i: integer;
begin
  if(time() = 1) then
  begin
    WriteStats(iniFile);
    WriteNotEmptySkills(iniFile);
    WriteSkillIncrease(iniFile);
    WriteLastJournalMessages(iniFile);
    
    lines := TStringList.Create;
    iniFile.getStrings(lines);
    //for i:= 0 to lines.Count-1 do
      //AddToSystemJournal(lines[i]);
    lines.Free;
    SendData(iniFile);
  end;
end;

begin
  AddToSystemJournal('stealthpage init');
  refreshPeriod := 10;//sec
  iniFile := TMemIniFile.Create('no.ini');
  initialSkills := TMemIniFile.Create('no2.ini');
  WriteNotEmptySkills(initialSkills);
  lastRecordedJournalLine := HighJournal;
  SetEventProc(evTimer2, 'StealthPageMain');
  AddToSystemJournal('stealthpage init done');
end. 
