import pytest
from src.valuation_engine import calculate_sensitivity, safe_ratio

def test_known_valuation_examples():
    result=calculate_sensitivity(250_000_000,20_000_000,5_000_000,1)
    assert result["ev_ebitda"]==12.5
    assert result["remediation_ev"]==pytest.approx(.02)
    assert result["adjusted_ev"]==245_000_000

def test_zero_ebitda_is_safe():
    result=calculate_sensitivity(250_000_000,0,5_000_000,.5)
    assert result["ev_ebitda"] is None and result["remediation_ebitda"] is None

def test_invalid_inputs():
    with pytest.raises(ValueError): calculate_sensitivity(-1,20,5,.5)
    with pytest.raises(ValueError): calculate_sensitivity(10,2,1,1.01)
    assert safe_ratio(0,10)==0
