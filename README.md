# visceral-poc

## Essential Integrations

### Logging Setup

Check that logging is properly set up for effective debugging.

- [ ] **Loki**
  - [ ] Confirm logs from this service are being captured by Loki.
  - [ ] Make sure alerts are configured for key log events.
- [x] **Logstash**
  - [x] Ensure Logstash is processing logs from this service correctly.

### Heartbeat Monitoring

Verify that heartbeat checks are active to ensure the service is operational.

- [ ] **ELK Stack**
  - [ ] Check that Elasticsearch is receiving heartbeat data.
  - [ ] Verify Kibana displays this service's heartbeat data correctly.

### Performance Monitoring

Ensure New Relic is monitoring the performance effectively.

- [ ] **New Relic Setup**
  - [ ] Check New Relic agents are active on this service.
  - [ ] Ensure alerts for performance issues are configured.
  - [ ] Verify deployment markers are used correctly for updates.

### Analytics Integration

Confirm analytics are providing insights into service usage.

- [ ] ~~**Google Analytics**~~
  - [ ] ~~Check integration is tracking user interactions correctly.~~
- [ ] ~~**RudderStack**~~
  - [ ] ~~Ensure data flows correctly into the analytics pipeline.~~

### Prometheus and Grafana Monitoring

Make sure metrics are being monitored and visualized properly.

- [ ] **Prometheus**
  - [x] \*Verify metrics collection is configured for this service.
  - [ ] Check that alerts are set up for any anomalies.
- [ ] **Grafana**
  - [ ] Confirm dashboards are showing accurate service metrics.

### Code Quality and Testing

Check that code quality and testing standards are met.

- [ ] **SonarQube**
  - [ ] Ensure code is regularly analyzed and meets quality standards.
- [ ] **Code Coverage**
  - [ ] Verify code coverage metrics meet the required threshold.
- [ ] **API Testing**
  - [ ] Confirm API tests are thorough and reflect current functionality.

### CI/CD Pipeline

Review the CI/CD setups to confirm they are efficient and accurate.

- [ ] **GitHub Actions**
  - [x] Ensure workflows are properly configured for continuous integration.
  - [ ] Check that builds and tests run successfully with each update.

