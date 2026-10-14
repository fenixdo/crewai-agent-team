# crewai-agent-team

Deployment chung trên CrewAI AMP cho **2 agent: Sale và HR** (gói Basic chỉ cho 2 crew: team + Marketing).

- Code của từng agent nằm ở repo riêng: [crewai-agent-sale](https://github.com/fenixdo/crewai-agent-sale), [crewai-agent-hr](https://github.com/fenixdo/crewai-agent-hr). Repo này cài chúng làm dependency git; `uv.lock` ghim commit cụ thể.
- AMP mở A2A cho từng agent: Marketing gọi `/a2a` với `metadata.target_agent` = slug vai trò của agent.
- `/kickoff` (input `proposal`) chạy Sale dự báo → HR lập kế hoạch nhân sự.

**Cập nhật một agent (ví dụ đổi chính sách giá của Sale):**
```bash
# 1. sửa + push repo crewai-agent-sale
# 2. ở đây: kéo commit mới vào lock rồi push → AMP tự redeploy
uv lock --upgrade-package crewai-agent-sale && git commit -am "Sale v2" && git push
```

```bash
uv sync --group dev && .venv/bin/pytest -q
.venv/bin/crewai deploy validate
```
