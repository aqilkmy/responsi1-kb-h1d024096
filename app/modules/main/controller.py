class MainController:
    def index(self):
        return {
            "title": "Asisten Pertanian Cerdas",
            "subtitle": "Sistem irigasi fuzzy dan sistem pakar diagnosis tanaman pangan",
        }

    @staticmethod
    def _triangular(x, a, b, c):
        if x <= a or x >= c:
            return 0.0
        if x == b:
            return 1.0
        if x < b:
            return (x - a) / (b - a)
        return (c - x) / (c - b)

    def irrigation_fuzzy(self, soil_moisture, temperature, humidity, rain_chance):
        moisture_low = self._triangular(soil_moisture, 0, 20, 50)
        moisture_medium = self._triangular(soil_moisture, 30, 50, 70)
        moisture_high = self._triangular(soil_moisture, 55, 80, 100)

        temp_low = self._triangular(temperature, 0, 16, 28)
        temp_medium = self._triangular(temperature, 22, 30, 38)
        temp_high = self._triangular(temperature, 32, 40, 50)

        humidity_low = self._triangular(humidity, 0, 25, 55)
        humidity_medium = self._triangular(humidity, 40, 60, 80)
        humidity_high = self._triangular(humidity, 65, 85, 100)

        rain_low = self._triangular(rain_chance, 0, 15, 40)
        rain_medium = self._triangular(rain_chance, 25, 50, 75)
        rain_high = self._triangular(rain_chance, 60, 85, 100)

        rules = [
            (min(moisture_low, temp_high, humidity_low, rain_low), 22),
            (min(moisture_low, temp_medium, rain_low), 18),
            (min(moisture_medium, temp_high, humidity_low, rain_low), 14),
            (min(moisture_medium, temp_medium, rain_medium), 10),
            (min(moisture_high, rain_low), 5),
            (max(moisture_high, rain_high, humidity_high), 0),
            (min(temp_low, moisture_medium), 6),
        ]

        weighted_sum = sum(strength * duration for strength, duration in rules)
        denominator = sum(strength for strength, _ in rules)

        duration_minutes = round(weighted_sum / denominator, 1) if denominator else 0.0

        if duration_minutes <= 2:
            action = "Pompa mati"
        elif duration_minutes <= 8:
            action = "Siram ringan"
        elif duration_minutes <= 15:
            action = "Siram sedang"
        else:
            action = "Siram intensif"

        return {
            "inputs": {
                "soil_moisture": soil_moisture,
                "temperature": temperature,
                "humidity": humidity,
                "rain_chance": rain_chance,
            },
            "duration_minutes": duration_minutes,
            "action": action,
        }

    def expert_diagnosis(self, selected_symptoms):
        knowledge_base = [
            {
                "name": "Wereng batang cokelat",
                "category": "Hama",
                "symptoms": {
                    "daun_menguning",
                    "serangga_coklat",
                    "tanaman_kerdil",
                    "bercak_hopperburn",
                },
                "advice": "Kurangi pupuk nitrogen berlebih, gunakan varietas tahan, dan aplikasikan insektisida selektif bila populasi tinggi.",
            },
            {
                "name": "Blast padi",
                "category": "Penyakit jamur",
                "symptoms": {
                    "bercak_belah_ketupat",
                    "daun_mengering",
                    "malai_hampa",
                },
                "advice": "Gunakan benih sehat, atur jarak tanam, dan semprot fungisida sesuai rekomendasi bila gejala meluas.",
            },
            {
                "name": "Hawar daun bakteri",
                "category": "Penyakit bakteri",
                "symptoms": {
                    "daun_layu",
                    "bercak_kuning_memanjang",
                    "ujung_daun_kering",
                },
                "advice": "Perbaiki drainase, hindari luka mekanis saat pemeliharaan, dan gunakan bakterisida sesuai anjuran.",
            },
            {
                "name": "Ulat grayak",
                "category": "Hama",
                "symptoms": {
                    "daun_berlubang",
                    "terlihat_ulat",
                    "serangan_malam",
                },
                "advice": "Lakukan monitoring malam hari, gunakan agen hayati, dan insektisida bila melewati ambang kendali.",
            },
            {
                "name": "Busuk akar",
                "category": "Penyakit jamur",
                "symptoms": {
                    "akar_membusuk",
                    "layu_meski_air_cukup",
                    "bau_busuk_tanah",
                },
                "advice": "Kurangi genangan, gunakan media tanam dengan aerasi baik, dan lakukan perlakuan fungisida akar.",
            },
        ]

        selected = set(selected_symptoms)
        results = []

        for rule in knowledge_base:
            match_count = len(rule["symptoms"] & selected)
            confidence = round((match_count / len(rule["symptoms"])) * 100, 1)
            if match_count > 0:
                results.append(
                    {
                        "name": rule["name"],
                        "category": rule["category"],
                        "confidence": confidence,
                        "matched_symptoms": sorted(rule["symptoms"] & selected),
                        "advice": rule["advice"],
                    }
                )

        results.sort(key=lambda item: item["confidence"], reverse=True)

        primary = results[0] if results else None
        if primary and primary["confidence"] < 40:
            primary = None

        return {
            "selected_symptoms": sorted(selected),
            "primary_diagnosis": primary,
            "all_possibilities": results,
        }
