import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Privacy Policy",
  description: "Privacy Policy for XingAI Passive Income Idea (passive.xingai.app).",
  alternates: { canonical: "/legal/privacy" },
};

const updated = "2026-09-28";

export default function PrivacyPage() {
  return (
    <article className="legal">
      <div>
        <h1>Privacy Policy · XingAI Passive Income Idea</h1>
        <p className="meta">Last updated: {updated}</p>
        <p>
          XingAI Passive Income Idea (“the Service”) publishes informational Idea research for a
          defined operator profile (web board, optional email Summary, A4 PDF). This policy describes
          what we collect for the public demo at passive.xingai.app.
        </p>
        <h2>1. Data we may process</h2>
        <p>
          Preference settings stored on your device (locale, theme). If you join a waitlist or email
          list later, we process the email address you provide. Published Idea pages may include
          publicly sourced citations (for example government or vendor documentation URLs) that you
          choose to open.
        </p>
        <h2>2. What we do not collect in this demo</h2>
        <p>
          The public demo does not connect Gmail, does not store app-owned todos, and does not
          require an account. Brokerage, tax IDs, and payment credentials are out of scope.
        </p>
        <h2>3. AI processing</h2>
        <p>
          Research drafts and Idea summaries may be generated with third-party AI providers during
          report production. Published pages are static snapshots. Do not paste secrets into any
          future prompt or contact form.
        </p>
        <h2>4. Cookies and local storage</h2>
        <p>
          We use local storage for locale and theme only. Analytics cookies may be added later and
          will be disclosed here before they ship.
        </p>
        <h2>5. Sharing</h2>
        <p>
          We do not sell personal data. Hosting providers (for example Vercel) process traffic as
          needed to serve the site. Email providers process addresses only if you opt in later.
        </p>
        <h2>6. Retention and contact</h2>
        <p>
          Device preferences stay until you clear site data. Waitlist emails (if any) are kept until
          you ask to be removed. Contact:{" "}
          <a href="mailto:contact@xingai.app">contact@xingai.app</a>.
        </p>
      </div>

      <hr />

      <div lang="zh-Hans">
        <h2 className="legal-lang-title">隐私政策</h2>
        <p className="meta">最后更新：{updated}</p>
        <p>
          XingAI Passive Income Idea（“本服务”）为特定运营者画像发布被动收入 Idea
          研究（网页看板、可选邮件 Summary、A4 PDF）。本文说明公开演示站点 passive.xingai.app
          的数据处理。
        </p>
        <h2>1. 可能处理的数据</h2>
        <p>
          设备上的偏好（语言、主题）。若你日后加入候补或邮件列表，我们处理你提供的邮箱。公开 Idea
          页可能包含你可自行打开的公开来源链接。
        </p>
        <h2>2. 本演示不收集的内容</h2>
        <p>不连接 Gmail、不存储待办、不要求账号。券商、税号与支付凭证均不在范围内。</p>
        <h2>3. AI 处理</h2>
        <p>报告生产阶段可能使用第三方 AI。已发布页面为静态快照。请勿把密钥粘贴进提示或联系表单。</p>
        <h2>4. Cookie 与本地存储</h2>
        <p>语言与主题使用本地存储。日后若增加分析 Cookie，会先更新本页。</p>
        <h2>5. 共享</h2>
        <p>我们不出售个人数据。托管商仅为提供站点处理流量；邮件服务仅在你主动订阅后处理邮箱。</p>
        <h2>6. 保留与联系</h2>
        <p>
          设备偏好直至你清除站点数据。候补邮箱可按请求删除。联系：
          <a href="mailto:contact@xingai.app">contact@xingai.app</a>。
        </p>
      </div>

      <hr />

      <div lang="ko">
        <h2 className="legal-lang-title">개인정보 처리방침</h2>
        <p className="meta">최종 업데이트: {updated}</p>
        <p>
          XingAI Passive Income Idea(“서비스”)는 정해진 운영자 프로필용 수동소득 Idea 리서치를
          게시합니다(웹 보드, 선택 메일 Summary, A4 PDF). 본 정책은 passive.xingai.app 공개 데모의
          처리 내용을 설명합니다.
        </p>
        <h2>1. 처리 가능 데이터</h2>
        <p>
          기기의 언어·테마 설정. 대기열/메일 목록에 가입하면 제공한 이메일을 처리합니다. 공개 Idea
          페이지에는 사용자가 열 수 있는 공개 출처 링크가 포함될 수 있습니다.
        </p>
        <h2>2. 이 데모에서 수집하지 않는 것</h2>
        <p>Gmail 연결, 앱 소유 할 일, 계정 로그인은 없습니다. 증권·세금·결제 정보는 범위 밖입니다.</p>
        <h2>3. AI 처리</h2>
        <p>리포트 생성 단계에서 제3자 AI가 쓰일 수 있습니다. 게시물은 정적 스냅샷입니다.</p>
        <h2>4. 쿠키·로컬 저장소</h2>
        <p>언어·테마만 로컬 저장소를 사용합니다. 분석 쿠키가 추가되면 이 페이지를 먼저 갱신합니다.</p>
        <h2>5. 공유</h2>
        <p>개인정보를 판매하지 않습니다. 호스팅은 사이트 제공 목적, 이메일은 옵트인 후에만 처리합니다.</p>
        <h2>6. 보관·문의</h2>
        <p>
          기기 설정은 사이트 데이터를 지울 때까지 유지됩니다. 대기열 이메일은 삭제 요청 시 제거합니다.
          문의: <a href="mailto:contact@xingai.app">contact@xingai.app</a>.
        </p>
      </div>

      <p className="meta" style={{ marginTop: "1.5rem" }}>
        <Link href="/legal/terms">Terms</Link>
        {" · "}
        <Link href="/legal/disclaimer">Disclaimer</Link>
      </p>
    </article>
  );
}
