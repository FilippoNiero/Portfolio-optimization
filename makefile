CC = g++

CFLAGS = -std=c++11 -Wall

# !!! Change with your paths for cplex

INCLUDES = -I/path/to/cplex/cplexXX/include -I/path/to/cplex/concertYY/include

LIB_DIRS = -Lpath/to/cplex/cplexXX/include -L/path/to/cplex/concertYY/lib/archi/tecture

LIBS = -lilocplex -lconcert -lcplex -lm -lpthread -ldl

MARKOWITZ_SRCS = markowitz.cpp 
CDD_SRCS = cdd.cpp 

MARKOWITZ_TARGET = markowitz
CDD_TARGET = cdd

INSTANCES_FILE = run_instances.txt

INSTANCES := $(shell cat $(INSTANCES_FILE))


all: $(MARKOWITZ_TARGET) $(CDD_TARGET)

$(MARKOWITZ_TARGET): $(MARKOWITZ_SRCS)
	$(CC) $(CFLAGS) $(INCLUDES) $(LIB_DIRS) -o $(MARKOWITZ_TARGET) $(MARKOWITZ_SRCS) $(LIBS)

$(CDD_TARGET): $(CDD_SRCS)
	$(CC) $(CFLAGS) $(INCLUDES) $(LIB_DIRS) -o $(CDD_TARGET) $(CDD_SRCS) $(LIBS)

clean:
	rm -f $(MARKOWITZ_TARGET) $(CDD_TARGET)

rebuild: clean all

run: all
	for instance in $(INSTANCES); do \
		./$(MARKOWITZ_TARGET) "$$instance"; \
		./$(CDD_TARGET) "$$instance"; \
	done
