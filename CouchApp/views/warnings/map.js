function(doc) {
    if(doc.Content && doc.File && doc.Host) {
        if(doc.Content.search(/warning/i) != -1){
            date_key = String(doc.Year) + String(doc.Month) + String(doc.Day);

            emit({date:date_key}, doc);
            emit({date:date_key, host:doc.Host}, doc);
            emit({date:date_key, host:doc.Host, file: doc.File}, doc);
        }
    }
}
