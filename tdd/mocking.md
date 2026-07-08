# 모킹 시기

**시스템 경계**에서만 모킹:

- 외부 API (결제, 이메일 등)
- 데이터베이스 (가끔 - 테스트 DB 선호)
- 시간/난수
- 파일 시스템 (가끔)

모킹하지 않을 것:

- 자신의 클래스/모듈
- 내부 협력자
- 당신이 통제하는 모든 것

## 모킹 가능성을 위한 설계

시스템 경계에서는 모킹하기 쉬운 인터페이스 설계:

**1. 의존성 주입 사용**

내부에서 생성하지 않고 외부 의존성 전달:

```typescript
// 모킹 쉬움
function processPayment(order, paymentClient) {
  return paymentClient.charge(order.total);
}

// 모킹 어려움
function processPayment(order) {
  const client = new StripeClient(process.env.STRIPE_KEY);
  return client.charge(order.total);
}
```

**2. 제네릭 페처보다 SDK 스타일 인터페이스 선호**

조건부 로직이 있는 하나의 제네릭 함수 대신 각 외부 작업에 특정 함수 생성:

```typescript
// 좋음: 각 함수를 독립적으로 모킹 가능
const api = {
  getUser: (id) => fetch(`/users/${id}`),
  getOrders: (userId) => fetch(`/users/${userId}/orders`),
  createOrder: (data) => fetch('/orders', { method: 'POST', body: data }),
};

// 나쁨: 모킹에 조건부 로직 필요
const api = {
  fetch: (endpoint, options) => fetch(endpoint, options),
};
```

SDK 접근법의 의미:
- 각 모킹이 하나의 특정 형태 반환
- 테스트 설정에 조건부 로직 없음
- 테스트가 어떤 엔드포인트를 실행하는지 쉽게 확인
- 엔드포인트별 타입 안전
