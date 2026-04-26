from app.modules.main.controller import MainController


def test_index():
    main_controller = MainController()
    result = main_controller.index()
    assert result["title"] == "Asisten Pertanian Cerdas"


def test_irrigation_fuzzy():
    main_controller = MainController()
    result = main_controller.irrigation_fuzzy(soil_moisture=20, temperature=36, humidity=35, rain_chance=15)
    assert result["duration_minutes"] >= 0
    assert result["action"] in {"Pompa mati", "Siram ringan", "Siram sedang", "Siram intensif"}


def test_expert_diagnosis():
    main_controller = MainController()
    result = main_controller.expert_diagnosis(["daun_menguning", "serangga_coklat", "tanaman_kerdil"])
    assert "all_possibilities" in result
    assert len(result["all_possibilities"]) > 0
