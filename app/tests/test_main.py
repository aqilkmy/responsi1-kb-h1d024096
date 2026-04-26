class TestMain():
    def test_index(self, client):
        response = client.get('/')
        assert response.status_code == 200
        assert b"Asisten Pertanian Cerdas" in response.data

    def test_fuzzy_route(self, client):
        response = client.post(
            '/fuzzy',
            data={
                'soil_moisture': 30,
                'temperature': 34,
                'humidity': 40,
                'rain_chance': 20,
            },
        )
        assert response.status_code == 200
        assert b"Durasi rekomendasi penyiraman" in response.data

    def test_expert_route(self, client):
        response = client.post(
            '/expert',
            data={
                'symptoms': ['daun_menguning', 'serangga_coklat', 'tanaman_kerdil'],
            },
        )
        assert response.status_code == 200
        assert b"Diagnosa" in response.data
            