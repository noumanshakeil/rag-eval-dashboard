import pytest
@pytest.mark.asyncio
async def test_run(client):
    c = await client.post("/api/cases", json={"question": "What is VPN?", "context": "VPN is required for staging."})
    r = await client.post(f"/api/cases/{c.json()['id']}/run")
    assert r.status_code == 200
    assert "faithfulness" in r.json()
