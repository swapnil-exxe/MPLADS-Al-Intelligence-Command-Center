# Demo Strategy & Storyline — WeatherGPT (SIH26068)

## 5 Master Live-Demo Scenarios

### Scenario 1: English Voice Query (Travel & Highway Safety)
- **Prompt**: *"Can I travel from Mumbai to Pune tomorrow afternoon?"*
- **Highlights**: STT transcription, 24h hourly rain graph, travel advisory card warning of low visibility between 2 PM and 6 PM.

### Scenario 2: Hindi Voice Query (Agriculture & Agromet Advisory)
- **Prompt**: *"क्या नाशिक में कल कपास की फसल पर कीटनाशक का छिड़काव करना सुरक्षित है?"*
- **Highlights**: Hindi STT & TTS, RAG Agromet bulletin lookup, voice response advising against spraying due to coming rain.

### Scenario 3: Marathi Voice Query (Marine / Coastal Safety)
- **Prompt**: *"रत्नागिरीमध्ये आज समुद्रात मासेमारीसाठी जाणे सुरक्षित आहे का?"*
- **Highlights**: Marathi STT & TTS, wind/wave threshold check, HIGH RISK card alert for coastal fishermen.

### Scenario 4: Dynamic Emergency Disaster Command Mode
- **Trigger**: Click "Simulate High Cyclone/Flood Risk" or search coastal hazard zone.
- **Highlights**: Dynamic UI morph to Red Emergency Command layout, active hazard warning, NDMA safety directives, emergency helpline numbers, danger radius on Leaflet map.

### Scenario 5: Historical Climate Comparison
- **Prompt**: *"Is this August temperature in Delhi normal compared to historical data?"*
- **Highlights**: Open-Meteo ERA5 30-year historical climate lookup, comparative temperature graph showing 2.8°C heat anomaly.
