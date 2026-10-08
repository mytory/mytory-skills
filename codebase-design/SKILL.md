---
name: codebase-design
description: 깊은 모듈을 설계하기 위한 공통 어휘입니다. "모듈 인터페이스 설계해줘", "모듈을 심화할 기회를 찾아줘", "seam을 어디에 둘까", "테스트하기 쉬운 구조로 바꿔줘", "AI가 탐색하기 쉬운 코드로 개선해줘"라고 할 때, 또는 다른 스킬에 깊은 모듈의 어휘가 필요할 때 사용합니다.
---

# 코드베이스 설계

**깊은 모듈**을 설계하세요. 작은 interface 뒤에 많은 동작을 넣고 명확한 seam에 배치하여 그 interface를 통해 테스트할 수 있게 합니다. 코드를 설계하거나 재구성할 때 이 용어와 원칙을 사용하세요. 목표는 호출자에게 leverage, 유지보수자에게 locality, 모두에게 테스트 용이성을 제공하는 것입니다.

## 용어집

다음 용어를 정확히 사용하세요. "component", "service", "API", "boundary"로 바꾸지 마세요. 일관된 언어를 쓰는 것이 핵심입니다.

**Module**: interface와 implementation이 있는 모든 것. 의도적으로 규모에 제한을 두지 않습니다. 함수, 클래스, 패키지, 여러 계층을 가로지르는 기능 단위일 수 있습니다. _피할 표현_: unit, component, service.

**Interface**: 호출자가 모듈을 올바르게 사용하려면 알아야 하는 모든 것. 타입 시그니처뿐 아니라 불변 조건, 호출 순서 제약, 오류 형태, 필요한 설정, 성능 특성도 포함합니다. _피할 표현_: API, signature(타입 수준의 표면만 가리키므로 너무 좁음).

**Implementation**: 모듈 내부의 코드와 구현 내용. **Adapter**와 구별하세요. Postgres 저장소처럼 작은 adapter에 큰 implementation이 있을 수도 있고, 메모리 기반 가짜 객체처럼 큰 adapter에 작은 implementation이 있을 수도 있습니다. seam이 논의의 주제일 때는 "adapter", 그 외에는 "implementation"을 사용하세요.

**Depth**: interface가 제공하는 leverage. 호출자(또는 테스트)가 배워야 하는 interface의 단위당 실행할 수 있는 동작의 양입니다. 작은 interface 뒤에 많은 동작이 있으면 모듈이 **deep**, interface가 implementation만큼 복잡하면 **shallow**입니다.

**Seam** _(Michael Feathers)_: 그곳의 코드를 수정하지 않고 동작을 바꿀 수 있는 지점. 모듈의 interface가 놓이는 *위치*입니다. seam을 어디에 둘지는 그 뒤에 무엇을 둘지와 별개의 설계 결정입니다. _피할 표현_: boundary(DDD의 bounded context와 의미가 겹침).

**Adapter**: seam에서 interface를 충족하는 구체적인 대상. 내부 내용이 아니라 맡은 *역할*(어떤 자리를 채우는지)을 설명합니다.

**Leverage**: 호출자가 depth에서 얻는 것. 알아야 할 interface의 단위당 더 많은 기능을 얻습니다. 하나의 implementation이 N개의 호출 지점과 M개의 테스트에 이익을 줍니다.

**Locality**: 유지보수자가 depth에서 얻는 것. 변경, 버그, 지식, 검증이 호출자 전반에 흩어지지 않고 한곳에 모입니다. 한 번 수정하면 모든 곳에 반영됩니다.

## 깊은 모듈과 얕은 모듈

**깊은 모듈** = 작은 interface + 많은 implementation:

```
┌─────────────────────┐
│   작은 Interface    │  ← 적은 메서드, 단순한 매개변수
├─────────────────────┤
│                     │
│   깊은 Implementation│ ← 복잡한 로직을 숨김
│                     │
└─────────────────────┘
```

**얕은 모듈** = 큰 interface + 적은 implementation(피할 것):

```
┌─────────────────────────────────┐
│       큰 Interface              │  ← 많은 메서드, 복잡한 매개변수
├─────────────────────────────────┤
│  얇은 Implementation            │  ← 단순 전달
└─────────────────────────────────┘
```

interface를 설계할 때 다음을 물으세요.

- 메서드 수를 줄일 수 있나요?
- 매개변수를 단순하게 만들 수 있나요?
- 더 많은 복잡성을 내부에 숨길 수 있나요?

## 원칙

- **Depth는 implementation이 아니라 interface의 속성입니다.** 깊은 모듈 내부는 작고 모킹하거나 교체하기 쉬운 부분들로 구성될 수 있습니다. 다만 그 부분들은 외부 interface에 속하지 않습니다. 모듈에는 자기 테스트가 사용하는 **내부 seam**(implementation에만 공개)과 interface에 놓인 **외부 seam**이 모두 있을 수 있습니다.
- **삭제 테스트.** 모듈을 삭제한다고 상상하세요. 복잡성이 사라진다면 단순 전달 계층이었습니다. 복잡성이 N개의 호출자로 다시 퍼진다면 제 역할을 하던 모듈입니다.
- **Interface가 테스트 표면입니다.** 호출자와 테스트는 같은 seam을 건넙니다. interface를 *넘어가서* 테스트해야 한다면 모듈의 형태가 잘못되었을 가능성이 큽니다.
- **Adapter 하나는 가상의 seam, 둘은 실제 seam입니다.** 실제로 그 지점에서 무언가 달라지지 않는다면 seam을 도입하지 마세요.

## 테스트 용이성을 위한 설계

좋은 interface는 자연스럽게 테스트할 수 있습니다.

1. **의존성을 생성하지 말고 전달받으세요.**

   ```typescript
   // 테스트하기 쉬움
   function processOrder(order, paymentGateway) {}

   // 테스트하기 어려움
   function processOrder(order) {
     const gateway = new StripeGateway();
   }
   ```

2. **부수 효과를 만들기보다 결과를 반환하세요.**

   ```typescript
   // 테스트하기 쉬움
   function calculateDiscount(cart): Discount {}

   // 테스트하기 어려움
   function applyDiscount(cart): void {
     cart.total -= discount;
   }
   ```

3. **작은 표면.** 메서드가 적으면 필요한 테스트도 줄어듭니다. 매개변수가 적으면 테스트 준비가 단순해집니다.

## 관계

- **Module**에는 호출자와 테스트에 보여주는 표면인 **Interface**가 정확히 하나 있습니다.
- **Depth**는 **Interface**를 기준으로 평가하는 **Module**의 속성입니다.
- **Seam**은 **Module**의 **Interface**가 놓이는 곳입니다.
- **Adapter**는 **Seam**에 놓여 **Interface**를 충족합니다.
- **Depth**는 호출자에게 **Leverage**, 유지보수자에게 **Locality**를 제공합니다.

## 채택하지 않는 설명

- **Implementation 줄 수와 interface 줄 수의 비율로 depth를 측정**(Ousterhout): implementation에 코드를 늘리는 것에 보상을 줍니다. 여기서는 leverage로 depth를 이해합니다.
- **"Interface"를 TypeScript `interface` 키워드나 클래스의 public 메서드로 한정**: 너무 좁습니다. 여기서 interface는 호출자가 알아야 할 모든 사실을 포함합니다.
- **"Boundary"**: DDD의 bounded context와 뜻이 겹칩니다. **seam**이나 **interface**라고 하세요.

## 더 살펴보기

- **의존성을 고려해 모듈 묶음을 심화하기**: [DEEPENING.md](DEEPENING.md)에서 의존성의 종류, seam 원칙, 계층을 추가하지 않고 교체하는 테스트를 살펴보세요.
- **대안 interface 탐색하기**: [DESIGN-IT-TWICE.md](DESIGN-IT-TWICE.md)에서 여러 하위 에이전트가 근본적으로 다른 interface를 병렬로 설계하고 depth, locality, seam 위치에 따라 비교하는 방법을 살펴보세요.
