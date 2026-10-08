# 좋은 테스트와 나쁜 테스트

## 좋은 테스트

**통합 스타일**: 내부 부분의 모킹이 아닌 실제 인터페이스를 통해 테스트.

```typescript
// 좋음: 관찰 가능한 동작을 테스트
test("유효한 장바구니로 체크아웃할 수 있다", async () => {
  const cart = createCart();
  cart.add(product);
  const result = await checkout(cart, paymentMethod);
  expect(result.status).toBe("confirmed");
});
```

특징:

- 사용자/호출자가 신경 쓰는 동작 테스트
- 공개 API만 사용
- 내부 리팩터에서 살아남음
- HOW가 아닌 WHAT을 설명
- 테스트당 하나의 논리적 단언

## 나쁜 테스트

**구현 세부사항 테스트**: 내부 구조에 결합.

```typescript
// 나쁨: 구현 세부사항을 테스트
test("체크아웃이 paymentService.process를 호출한다", async () => {
  const mockPayment = jest.mock(paymentService);
  await checkout(cart, payment);
  expect(mockPayment.process).toHaveBeenCalledWith(cart.total);
});
```

위험 신호:

- 내부 협력자를 모킹
- 비공개 메서드 테스트
- 호출 횟수/순서 단언
- 동작 변경 없이 리팩터링 시 테스트 깨짐
- 테스트명이 WHAT이 아닌 HOW 설명
- 인터페이스 대신 외부 수단으로 검증

```typescript
// 나쁨: 인터페이스를 우회하여 검증
test("createUser가 데이터베이스에 저장한다", async () => {
  await createUser({ name: "Alice" });
  const row = await db.query("SELECT * FROM users WHERE name = ?", ["Alice"]);
  expect(row).toBeDefined();
});

// 좋음: 인터페이스를 통해 검증
test("createUser가 사용자를 조회 가능하게 만든다", async () => {
  const user = await createUser({ name: "Alice" });
  const retrieved = await getUser(user.id);
  expect(retrieved.name).toBe("Alice");
});
```

**동어반복 테스트**: 기대값을 구현과 같은 방식으로 계산하면 구조상 통과하도록 만들어진 테스트입니다.

```typescript
// 나쁨: 코드와 같은 방식으로 기대값 계산
test("calculateTotal이 항목 금액을 합산한다", () => {
  const items = [{ price: 10 }, { price: 5 }];
  const expected = items.reduce((sum, item) => sum + item.price, 0);
  expect(calculateTotal(items)).toBe(expected);
});

// 좋음: 독립적으로 알려진 정답 사용
test("calculateTotal이 항목 금액을 합산한다", () => {
  expect(calculateTotal([{ price: 10 }, { price: 5 }])).toBe(15);
});
```
