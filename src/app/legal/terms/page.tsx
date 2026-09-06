import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Terms of Service",
  description: "Terms of Service for XingAI Passive Income Idea (daily.xingai.app).",
  alternates: { canonical: "/legal/terms" },
};

const updated = "2026-09-06";

export default function TermsPage() {
  return (
    <article className="legal">
      <div>
        <h1>Terms of Service</h1>
        <p className="meta">Last updated: {updated}</p>
        <p>
          By using XingAI Passive Income Idea you agree to these terms. The Service is provided for
          personal productivity assistance.
        </p>
        <h2>1. Acceptable use</h2>
        <p>
          Do not use the Service to spam, harass, violate others’ privacy, or break email/provider
          policies. You are responsible for content you approve to send.
        </p>
        <h2>2. No auto-send</h2>
        <p>
          Drafts are suggestions. The product is designed so outbound mail requires your explicit
          approval. You remain the sender of record for any mail you authorize.
        </p>
        <h2>3. AI output</h2>
        <p>
          Briefs, rankings, and drafts can be wrong or incomplete. Verify before acting.
        </p>
        <h2>4. Availability</h2>
        <p>
          The Service is provided “as is.” Features marked Soon may change or never ship.
        </p>
        <h2>5. Limitation of liability</h2>
        <p>
          To the fullest extent permitted by law, XingAI is not liable for losses from use of or
          reliance on the Service, including missed messages or incorrect drafts.
        </p>
        <h2>6. Contact</h2>
        <p>
          <a href="mailto:contact@xingai.app">contact@xingai.app</a>
        </p>
      </div>

      <hr />

      <div lang="zh-Hans">
        <h1>服务条款</h1>
        <p className="meta">最后更新：{updated}</p>
        <p>使用 XingAI Passive Income Idea 即表示你同意本条款。本服务用于个人生产力辅助。</p>
        <h2>1. 合理使用</h2>
        <p>不得用于骚扰、垃圾邮件、侵犯隐私或违反邮箱服务商政策。你对批准发送的内容负责。</p>
        <h2>2. 不自动发送</h2>
        <p>草稿仅为建议。出站邮件需你明确批准。你授权发送的邮件由你作为发送方负责。</p>
        <h2>3. AI 输出</h2>
        <p>简报、排序与草稿可能有误或不完整。行动前请核实。</p>
        <h2>4. 可用性</h2>
        <p>服务按“现状”提供。标记为即将推出的功能可能变更或永不发布。</p>
        <h2>5. 责任限制</h2>
        <p>在法律允许的最大范围内，XingAI 不对使用或依赖本服务造成的损失负责。</p>
        <h2>6. 联系</h2>
        <p>
          <a href="mailto:contact@xingai.app">contact@xingai.app</a>
        </p>
      </div>

      <hr />

      <div lang="ko">
        <h1>이용약관</h1>
        <p className="meta">최종 업데이트: {updated}</p>
        <p>XingAI Passive Income Idea 사용 시 본 약관에 동의합니다. 개인 생산성 지원 목적입니다.</p>
        <h2>1. 허용 사용</h2>
        <p>스팸·괴롭힘·프라이버시 침해·메일 제공자 정책 위반에 사용하지 마세요. 승인 발송 내용은 사용자 책임입니다.</p>
        <h2>2. 자동 발송 없음</h2>
        <p>초안은 제안입니다. 발송에는 명시적 승인이 필요합니다.</p>
        <h2>3. AI 출력</h2>
        <p>브리프·순위·초안은 틀리거나 불완전할 수 있습니다. 실행 전 확인하세요.</p>
        <h2>4. 가용성</h2>
        <p>서비스는 “있는 그대로” 제공됩니다. Soon 기능은 변경되거나 출시되지 않을 수 있습니다.</p>
        <h2>5. 책임 제한</h2>
        <p>법이 허용하는 범위에서 XingAI는 서비스 사용·의존으로 인한 손해에 책임지지 않습니다.</p>
        <h2>6. 문의</h2>
        <p>
          <a href="mailto:contact@xingai.app">contact@xingai.app</a>
        </p>
      </div>

      <p className="meta" style={{ marginTop: "1.5rem" }}>
        <Link href="/legal/privacy">Privacy</Link>
        {" · "}
        <Link href="/legal/disclaimer">Disclaimer</Link>
      </p>
    </article>
  );
}
