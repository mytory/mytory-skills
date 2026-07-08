# CONTEXT.md 형식

## 구조

```md
# {컨텍스트 이름}

{이 컨텍스트가 무엇이고 왜 존재하는지에 대한 한두 문장 설명.}

## 언어

**Order**:
{용어에 대한 한두 문장 설명}
_피할 것_: Purchase, transaction

**Invoice**:
배송 후 고객에게 발송되는 지불 요청.
_피할 것_: Bill, payment request

**Customer**:
주문을 하는 사람 또는 조직.
_피할 것_: Client, buyer, account
```

## 규칙

- **주관적이세요.** 같은 개념에 여러 단어가 있으면 가장 좋은 것을 고르고 나머지는 `_피할 것_` 아래에 나열.
- **정의는 간결하게.** 최대 한두 문장. 무엇인지 정의하고, 무엇을 하는지 정의하지 않음.
- **이 프로젝트의 컨텍스트에 특정된 용어만 포함.** 프로젝트가 광범위하게 사용하더라도 일반 프로그래밍 개념(타임아웃, 오류 유형, 유틸리티 패턴)은 속하지 않음. 용어를 추가하기 전에 자문: 이 개념이 이 컨텍스트에 고유한가, 아니면 일반 프로그래밍 개념인가? 전자만 속함.
- **자연스러운 군집이 생기면 하위 제목 아래에 용어 그룹화.** 모든 용어가 단일 응집 영역에 속하면 평면 목록으로 충분.

## 단일 vs 다중 컨텍스트 저장소

**단일 컨텍스트 (대부분의 저장소):** 저장소 루트에 하나의 `CONTEXT.md`.

**다중 컨텍스트:** 저장소 루트의 `CONTEXT-MAP.md`가 컨텍스트, 위치, 상호 관계를 나열:

```md
# 컨텍스트 맵

## 컨텍스트

- [Ordering](./src/ordering/CONTEXT.md) — 고객 주문 접수 및 추적
- [Billing](./src/billing/CONTEXT.md) — 인보이스 생성 및 결제 처리
- [Fulfillment](./src/fulfillment/CONTEXT.md) — 창고 피킹 및 배송 관리

## 관계

- **Ordering → Fulfillment**: Ordering이 `OrderPlaced` 이벤트 발행; Fulfillment가 이를 소비하여 피킹 시작
- **Fulfillment → Billing**: Fulfillment가 `ShipmentDispatched` 이벤트 발행; Billing이 이를 소비하여 인보이스 생성
- **Ordering ↔ Billing**: `CustomerId`와 `Money`에 대한 공유 타입
```

스킬은 어떤 구조가 적용되는지 추론:

- `CONTEXT-MAP.md`가 있으면, 읽어서 컨텍스트 찾기
- 루트 `CONTEXT.md`만 있으면, 단일 컨텍스트
- 둘 다 없으면, 첫 용어가 정리될 때 루트 `CONTEXT.md`를 게으르게 생성

다중 컨텍스트가 존재하면 현재 주제가 어느 것과 관련된지 추론. 불분명하면 물어보기.
