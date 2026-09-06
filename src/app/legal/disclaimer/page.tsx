import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Disclaimer",
  description:
    "Disclaimer for XingAI Passive Income Idea — informational only; not financial, tax, or business advice; no income guarantees.",
  alternates: { canonical: "/legal/disclaimer" },
};

const updated = "2026-09-06";

export default function DisclaimerPage() {
  return (
    <article className="legal">
      <div>
        <h1>Disclaimer</h1>
        <p className="meta">Last updated: {updated}</p>
        <h2>1. Informational only</h2>
        <p>
          Passive Income Idea 智报 content (Ideas, income bands, timelines, PDF/email) is for
          education and personal research. It is not financial, tax, legal, or business advice and
          does not create a professional relationship with XingAI.
        </p>
        <h2>2. No income guarantees</h2>
        <p>
          Projected ranges are estimates when sourced. Investment returns and business revenue are
          different. High yields are not real returns. Unverified items are labeled 未核实 — treat
          them as unknown.
        </p>
        <h2>3. You own the decisions</h2>
        <p>
          Starting a business, investing capital, or spending time is solely your responsibility.
          Verify sources, local law (including US / Texas where relevant), and risk before acting.
        </p>
        <h2>4. No warranty</h2>
        <p>The Service is provided “as is.” XingAI accepts no liability for outcomes from use of reports or code.</p>
        <h2>5. Contact</h2>
        <p>
          <a href="mailto:contact@xingai.app">contact@xingai.app</a>
        </p>
      </div>

      <hr />

      <div lang="zh-Hans">
        <h1>免责声明</h1>
        <p className="meta">最后更新：{updated}</p>
        <h2>1. 仅供参考</h2>
        <p>
          被动收入 Idea 智报（Idea、收入区间、时间线、PDF/邮件）仅供学习与个人研究，不构成金融、税务、法律或商业建议，亦不与 XingAI 形成专业关系。
        </p>
        <h2>2. 不保证收入</h2>
        <p>
          区间仅为有来源时的估计。投资收益与商业收入不同。高分红不等于真实回报。标「未核实」的内容视为未知。
        </p>
        <h2>3. 决策自负</h2>
        <p>创业、投资或投入时间均由你自行负责。行动前请核实来源与当地法规。</p>
        <h2>4. 无担保</h2>
        <p>服务按“现状”提供。XingAI 不对报告或代码使用后果承担责任。</p>
        <h2>5. 联系</h2>
        <p>
          <a href="mailto:contact@xingai.app">contact@xingai.app</a>
        </p>
      </div>

      <hr />

      <div lang="ko">
        <h1>면책조항</h1>
        <p className="meta">최종 업데이트: {updated}</p>
        <h2>1. 정보 제공용</h2>
        <p>
          수동소득 Idea 지보(아이디어, 수입 구간, 일정, PDF/메일)는 교육·개인 연구용이며 금융·세무·법률·사업 조언이 아니고 XingAI와의 전문 관계를 만들지 않습니다.
        </p>
        <h2>2. 수입 보장 없음</h2>
        <p>
          구간은 출처가 있을 때의 추정입니다. 투자 수익과 사업 매출은 다릅니다. 고배당 ≠ 실제 수익. 未核实는 미확인으로 취급하세요.
        </p>
        <h2>3. 결정은 사용자 책임</h2>
        <p>사업 시작·투자·시간 투입은 전적으로 사용자 책임입니다. 실행 전 출처와 현지 법을 확인하세요.</p>
        <h2>4. 보증 없음</h2>
        <p>서비스는 “있는 그대로” 제공됩니다.</p>
        <h2>5. 문의</h2>
        <p>
          <a href="mailto:contact@xingai.app">contact@xingai.app</a>
        </p>
      </div>

      <p className="meta" style={{ marginTop: "1.5rem" }}>
        <Link href="/legal/privacy">Privacy</Link>
        {" · "}
        <Link href="/legal/terms">Terms</Link>
      </p>
    </article>
  );
}
