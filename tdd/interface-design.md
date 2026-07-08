# 테스트 가능성을 위한 인터페이스 설계

좋은 인터페이스는 테스트를 자연스럽게 만듦:

1. **의존성을 받아들이고, 생성하지 말 것**

   ```typescript
   // 테스트 가능
   function processOrder(order, paymentGateway) {}

   // 테스트 어려움
   function processOrder(order) {
     const gateway = new StripeGateway();
   }
   ```

2. **결과를 반환하고, 부작용을 만들지 말 것**

   ```typescript
   // 테스트 가능
   function calculateDiscount(cart): Discount {}

   // 테스트 어려움
   function applyDiscount(cart): void {
     cart.total -= discount;
   }
   ```

3. **작은 표면적**
   - 적은 메서드 = 적은 테스트 필요
   - 적은 매개변수 = 더 단순한 테스트 설정
