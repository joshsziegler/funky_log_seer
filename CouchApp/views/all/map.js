function(doc) {
  if (doc.Content && doc.Host && doc.File) {
    var datekey = String(doc.Year) + String(doc.Month) + String(doc.Day);
    
    emit({date:datekey}, doc);
    emit({date:datekey, host:doc.Host}, doc);
    emit({date:datekey, host:doc.Host, file: doc.File}, doc);
  }
};
