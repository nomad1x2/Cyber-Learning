# DevOps Testing Automation

Automated tests within DevOps workflows to validate software quality, accelerate delivery, and reduce human error
- Catch bugs and vulnerabilities sooner rather than later

## Important things to consider

A good testing strategy is important
- Identifying testable components, defining test cases, and selecting appropriate automation tools

A good CI/CD pipeline is important
- Integrate automated tests into the build and deployment process

A solid team with skills in both development and testing automation could help

## Continuous Integration/Continuous Delivery/Deployment (CI/CD)

Continuous integration
- practice of automatically and frequently integrating code changes into a shared source code repository

Continuous delivery/deployment
- integration, testing, and delivery of code changes

Helps organizations avoid bugs and code failures while maintaining a continuous cycle of software development and updates

## Test automation stages

Unit testing
- Involves isolating your application into units and then testing the behavior of each as a function independent from external parties, databases, or configurations
- Often occurs during the build period and is considered the first layer of testing

Integration testing
- Integration testing evaluates how several units are logically integrated, and how this affects the system functionality without unintended errors in the integration process
- Testing the compliance of a system by verifying how disparate modules work together

Regression testing
- Ensures that bug fixes or other changes have not adversely affected existing functionality
- Allows developers to quickly and efficiently identify and fix any issues that may have been introduced by code changes, ensuring that the software remains reliable and bug free

End-to-end testing
- Tests the functionality and performance of the application by simulating the users expectations and needs from start to finish
- The end goal isn’t just to ensure the application validates and checks all the users needs, but to ensure it operates and behaves at least as well as expected

Exploratory testing
- More sophisticated software testing strategy that involves parallel learning, testing, and reviewing various functional and visual components from the users perspective

## DevSecOps

The practice of integrating security testing at every stage of the software development process

| Tool type | What it be doing |
|-----------|-------------|
| Static application security testing (SAST)| Analyze and find vulnerabilities in proprietary source code |
| Software composition analysis (SCA)| Automating visibility into open-source software use for the purpose of risk management, security, and license compliance |
| Interactive application security testing (IAST)| Evaluate an application’s potential vulnerabilities in the production environment |
| Dynamic application security testing (DAST)| Mimic hackers by testing the application's security from outside the network |

Ref:
- https://aws.amazon.com/what-is/devsecops/

## Benefits

- Increased test coverage, more frequent and comprehensive testing
  - Earlier bug detection, cheaper to fix in dev than in prod
  
- Consistency and reliability
  - Removes human error inherent in manual testing
  
- Strengthened collaboration between development and QA teams

- Simplified scaling across decentralized and cross-functional teams

- Faster and more reliable releases

- Easier and more proactive incident management

## Challenges

- Initial setup and maintenance can be expensive and time consuming
  - Cost of tools, training, and infrastructure should be factored in
  
- Not all tests are easily automated
  - Complex UI tests require significant effort and are still prone to failure from UI changes
  
- Over reliance on automation can lead to neglecting exploratory testing
  - Exploratory testing is important for catching unexpected issues

## Other References

- https://about.gitlab.com/topics/devops/devops-test-automation/
- https://dev.to/godofgeeks/testing-automation-in-devops-2i0
